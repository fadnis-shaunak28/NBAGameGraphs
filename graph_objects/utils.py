import polars as pl
import pandas as pd
import nba_api.stats.endpoints as nba_stats
import nba_api.live.nba.endpoints as nba_live
from nba_api.stats.static import players, teams
import re
from datetime import datetime as dt

# relevant pbp2 columns
pbp2_cols = [
            "EVENTNUM",
            "PLAYER1_ID",
            "PLAYER1_NAME",
            "PLAYER1_TEAM_ID",
            "PLAYER2_ID",
            "PLAYER2_NAME",
            "PLAYER2_TEAM_ID",
            "PLAYER3_ID",
            "PLAYER3_NAME",
            "PLAYER3_TEAM_ID",
            "PERIOD",
            "PCTIMESTRING"
            ]

# relevant pbp3 columns
pbp3_cols = [
            "actionNumber",
            "description",
            "actionType",
            "subType",
            "location",
            "scoreHome",
            "scoreAway",
            "shotDistance"
            ]

'''
Function for creating selected variable play-by-play dataframe

NOTE: This only works for already played games. Need to add extra time checking so that it calls the nba_live.PlayByPlay() endpoint instead of nba_stats

'''

def dfPolarsTest(g_id : str):
    # TODO: need to add function to get home_team from 
    # home_team = 1610612758
    try:
        # pull initial data for pbp tables, need V3 for action description and V2 for player identification
        pbp_3_raw = nba_stats.PlayByPlayV3(game_id=g_id)
        pbp_2_raw = nba_stats.PlayByPlayV2(game_id=g_id)

        # creating filtered pbp2 df
        pbp2_df = pbp_2_raw.get_data_frames()[0]
        pbp2_df_filtered = pl.from_pandas(pbp2_df).select(pbp2_cols)

        # creating filtered pbp3 df
        pbp3_df = pbp_3_raw.get_data_frames()[0]
        pbp3_df_filtered = pl.from_pandas(pbp3_df).select(pbp3_cols).rename({"actionNumber" : "EVENTNUM"})

        # merging two dfs for player and action details
        play_by_play_df = pbp3_df_filtered.join(pbp2_df_filtered, on="EVENTNUM", how="inner").lazy()
        
        df_clean = play_by_play_df.group_by("EVENTNUM").agg([
            pl.col("PERIOD").first(),
            pl.col("PCTIMESTRING").first(),
            pl.col("description").str.to_uppercase().str.concat(";"), # Concatenate all,
            pl.col("actionType").str.to_uppercase().str.concat(";"), # Concatenate all,
            pl.col("subType").str.to_uppercase().str.concat(";"), # Concatenate all,
            
            pl.col("PLAYER1_ID").first(),  # first P1 ID
            pl.col("PLAYER1_TEAM_ID").first(),  # first P1 team ID
            
            pl.col("PLAYER2_ID").last(), # last P2 ID
            pl.col("PLAYER2_TEAM_ID").first(),  # first P2 team ID
            
            pl.col("PLAYER3_ID").last(), # last P3 ID
            pl.col("PLAYER3_TEAM_ID").first(),  # first P3 team ID

            pl.col("scoreHome").max(), # post-action,
            pl.col("scoreAway").max(), # post-action,
            pl.col("shotDistance").max() # post-action
        ]).sort("EVENTNUM")
        
        pbp_downcast = df_clean.with_columns(
            ((pl.col("PCTIMESTRING").str.split(":").list.get(0).cast(pl.Int16) * 60) + (pl.col("PCTIMESTRING").str.split(":").list.get(1).cast(pl.Int16))),
            
            pl.col("PLAYER1_TEAM_ID").cast(pl.Int32),
            pl.col("PLAYER2_TEAM_ID").cast(pl.Int32),
            pl.col("PLAYER3_TEAM_ID").cast(pl.Int32),
            # pl.col("PLAYER1_TEAM_ID").eq(home_team).cast(pl.Int8).alias("HOME_AWAY_BOOL"),
            
            ## fill the scores forward, get around empty string with Null replace
            pl.col("scoreHome").replace("", None).cast(pl.Int16).forward_fill(),
            pl.col("scoreAway").replace("", None).cast(pl.Int16).forward_fill(),
            
            
            # type checking for action, cast to int from following mapping:
            # STL = 1
            # BLK = 2
            # MAKE = 3
            # MISS = 4
            # TURNOVER = 5
            # FOUL = 6
            # FT_MISS = 7
            # FT_MAKE = 8
            # REB = 9
            # TECH_FOUL = 10

            pl.when(pl.col("actionType").str.contains("MISS"))
            .then(
                pl.when(pl.col("actionType").str.contains(";"))
                .then(2)
                .otherwise(4)
            )
            .when(pl.col("actionType").str.contains("FREE"))
            .then(
                pl.when(pl.col("description").str.contains("MISS"))
                .then(7)
                .otherwise(8)
            )
            .when(pl.col("actionType").str.contains("TURNOVER"))
            .then(
                pl.when(pl.col("actionType").str.contains(";"))
                .then(1)
                .otherwise(5)
            )
            
            .when(pl.col("actionType").str.contains("FOUL"))
            .then(
                pl.when(pl.col("subType").str.contains("TECH"))
                .then(10)
                .when(pl.col("subType").str.contains("OFFENSIVE"))
                .then(5)
                .otherwise(6)
            )
            
            .when(pl.col("actionType").str.contains("REBOUND"))
            .then(9)
            
            .when(pl.col("actionType").str.contains("MADE"))
            .then(3)
            
            .otherwise(-1)
            
            .alias("PLAY_ACTION").cast(pl.Int8)           
        )
        
        
        pbp_df_final = pbp_downcast.filter(pl.col("PLAYER1_TEAM_ID").is_not_null()).collect()    
        return pbp_df_final
    
    except Exception as e:
        print(f"ERROR PROCESSING GAME - {g_id}: {e} ; PROCEEDING TO NEXT")
        return -1



'''
Function for scraping specific stats from event in pbp_df

px_action = return str denoting the stat to adjust in the playernode
player_direction = indicates whether edge is from p1 to px or px to p1; 
                    1 = p1 -> px, 
                    0 = px -> p1

'''


def scrapeActionType(action_type_str, p1_bool=False, p2_bool=False, p3_bool=False, miss_bool=None):
    p1_action = None
    p2_action = None
    p3_action = None
    player_direction = 1
    
    if p1_bool:
        # If Missed: P3 indicates a Block, else we don't return an action
        if "MISSED SHOT" in action_type_str:
            if p3_bool:
                p3_action = "BLK"
                player_direction = 0
                

        # If Made: p2 existence means assist
        elif "MADE SHOT" in action_type_str:
            p1_action = "PTS"
            if p2_bool:
                p2_action = "AST"
                player_direction = 0
                
        # If FT: MISS at start of string indicates miss so no PTS update
        elif "FREE THROW" in action_type_str:
            if not miss_bool:
                p1_action = "FT_MAKE"
                
        # If Rebound, just update REB
        elif "REBOUND" in action_type_str:
            p1_action = "REB"
            
        # 4 conditions for foul: Personal, Shooting, Flagrant, Technical
        elif "FOUL" in action_type_str:
            if p2_bool:
                p1_action = "PF"
                p2_action = "F_DRAWN"
            else:
                p1_action = "F_TECH"
                
        # elif "SUBSTITUTION" in action_type_str:
        #     p1_action = "SUB_OUT"
        #     p2_action = "SUB_IN"
        #     player_direction = 0
            
        elif "TURNOVER" in action_type_str:
            p1_action = "TO"
            if p2_bool:
                p2_action = "STL"
                player_direction = 0
                
    return p1_action, p2_action, p3_action, player_direction


def getGamesByDate(selected_date):
    # reformat the date from YYYY-MM-DD to M/D/YYYY
    date_obj = dt.strptime(selected_date, "%Y-%m-%d")
    new_date = date_obj.strftime("%#m/%#d/%Y")
    
    # get game informatin from scoreboard api endpoint
    games_raw = nba_stats.ScoreboardV2(game_date=new_date).get_data_frames()[0]
    game_cols = ["GAME_ID", "HOME_TEAM_ID", "VISITOR_TEAM_ID"]
    
    # records including home/away id and game id -> going to add callback for generating graph from clicking on the results
    games_simple = games_raw[game_cols].to_dict(orient='records')
    return games_simple
