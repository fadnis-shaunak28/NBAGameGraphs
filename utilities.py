import polars as pl
import nba_api.stats.endpoints as nba_stats
import nba_api.live.nba.endpoints as nba_live
from nba_api.stats.static import players, teams
from matplotlib import pyplot as plt

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

def create_clean_PBP_df(g_id : str):
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
    play_by_play_df = pbp3_df_filtered.join(pbp2_df_filtered, on="EVENTNUM", how="inner")
    
    df_clean = play_by_play_df.group_by("EVENTNUM").agg([
        pl.col("PERIOD").first(),
        pl.col("PCTIMESTRING").first(),
        pl.col("description").str.concat(";"), # Concatenate all,
        pl.col("actionType").str.concat(";"), # Concatenate all,
        pl.col("subType").str.concat(";"), # Concatenate all,
        
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
                                                pl.col("PLAYER1_TEAM_ID").cast(pl.Int32),
                                                pl.col("PLAYER2_TEAM_ID").cast(pl.Int32),
                                                pl.col("PLAYER3_TEAM_ID").cast(pl.Int32)
                                                )

    pre = play_by_play_df.estimated_size()
    post = pbp_downcast.estimated_size()

    print(f"pre downcast size {pre} \npost downcast size {post}")
    
    return pbp_downcast



'''
Function for scraping specific stats from event in pbp_df

'''

NODE_ACTION_STATS_DICT = {
    ""
}

EDGE_ACTION_STATS_DICT = {
    
}

def scrapeActionType(action_type_str, description_str):
    