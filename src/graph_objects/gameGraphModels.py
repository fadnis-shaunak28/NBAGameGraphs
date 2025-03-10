from dataclasses import dataclass, field
import nba_api.stats.endpoints as nba_stats
import nba_api.live.nba.endpoints as nba_live
from nba_api.stats.static import players, teams
from graph_objects import utils
# import utils
from typing import Dict, List, Tuple
import polars as pl
import re
import time
import joblib
import numpy as np
import bisect
from pathlib import Path
import json


TEAM_VIEW_TYPE = "TEAM"
DEFENSE_VIEW_TYPE = "DEFENSE"
    
EVENTNUM_INDEX = 0
PERIOD_INDEX = 1
PCTIMESTRING_INDEX = 2
DESCRIPTION_INDEX = 3
ACTION_TYPE_INDEX = 4
SUB_TYPE_INDEX = 5
P1_ID_INDEX = 6
P1_TEAM_ID_INDEX = 7
P2_ID_INDEX = 8
P2_TEAM_ID_INDEX = 9 
P3_ID_INDEX = 10
P3_TEAM_ID_INDEX = 11
SCORE_HOME_INDEX = 12
SCORE_AWAY_INDEX = 13
SHOT_DISTANCE_INDEX = 14
PLAY_ACTION_INDEX = 15

with open("src\graph_objects\jersey_nums_by_id.txt", 'r') as f:
    jersey_numbers_dict = json.load(f)


@dataclass
class gameEdge:
    # required attributes for init args
    to_p_id : int
    offense : bool

    # default stats set to 0
    AST : int = 0
    AST_PTS : int = 0
    STL : int = 0
    BLK : int = 0
    PF : int = 0    
    wpa_absolute : float = 0
    
    def __repr__(self):
        return f"Edge to {self.to_p_id}; Offense: {self.offense}"
    
    def __hash__(self):
        return hash(self.to_p_id)
    
    def updateStatsEdge(self, action_stat : int, wp_change : float, **kwargs):
        self.wpa_absolute = wp_change
        
        if action_stat == 1:
            self.STL += 1
        elif action_stat == 2:
            self.BLK += 1
        elif action_stat == 3:
            self.AST += 1
            if kwargs.get("three_made"):
                self.AST_PTS += 3
            else:
                self.AST_PTS += 2
        elif action_stat == 6:
            self.PF += 1

            
    def getEdgeStats(self):
        if self.offense:
            stats = {
                "AST" : self.AST,
                "AST_PTS" : self.AST_PTS ,
            }
        else:
            stats = {
                "STL" : self.STL,
                "BLK" : self.BLK,
                "PF" : self.PF,
            }
        stats["WPA"] = self.wpa_absolute
        
        return stats
    
    

@dataclass
class playerNode:
    # required attributes for init args
    id : int
    full_name : str
    display_name : str
    team_id : int
    
    # default stats set to 0/empty
    PTS : int = 0
    AST : int = 0
    REB : int = 0
    STL : int = 0
    BLK : int = 0
    TO : int = 0
    PF : int = 0
    F_DRAWN : int = 0
    F_TECH : int = 0
    
    # WPA Stats
    wpa_absolute : float = 0
    wpa_net : float = 0
    
    connections : Dict[str, gameEdge] = field(default_factory=dict)      # collection of edges out for a player, action is of form: this_player -> other_player
    
    def __repr__(self):
        return f"Player_ID: {self.id}, Player_Name: {self.full_name}"
    
    def __hash__(self):
        return hash(self.id) # hash on player ID for game
    
    def __eq__(self, other):
        if not isinstance(other, playerNode):
            return False
        
        return self.id == other.id

    def getPlayerStats(self):
        stats_dict = {
            "PTS" : self.PTS,
            "AST" : self.AST,
            "REB" : self.REB,
            "STL" : self.STL,
            "BLK" : self.BLK,
            "TO" : self.TO,
            "PF" : self.PF,
            "WPA_NET" : self.wpa_net,
            "WPA_ABS" : self.wpa_absolute
        }
        
        return stats_dict

    def gameEdgeGetOrAdd(self, to_pid, off_bool : bool):
        game_edge = self.connections.setdefault(to_pid, gameEdge(to_p_id=to_pid, offense=off_bool))
        return game_edge
    
        
                
class gameGraphBase:
    def __init__(self, game_id, home_team_id, away_team_id):
        self.game_id = game_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_score = 0
        self.away_score = 0
        
        self.graph_nodes = {}
        
        # Get the directory containing the current file
        current_dir = Path(__file__).parent
        # Go up one level to project root and then into wpa_model
        model_path = current_dir.parent / 'wpa_model' / 'wpa_model.pkl'
        
        self.wpa_model = joblib.load(str(model_path))
        
        # self.wpa_model = joblib.load("../wpa_model/wpa_model.pkl")
        self.wpa_rankings: List[Tuple[float, int]] = []
        self.wpa_max = float('-inf')
        self.wpa_min = float('inf')
        
        
    def get_wpa_rankings(self):
        return [(self.graph_nodes[pid].full_name, wpa) 
                    for pid, wpa in reversed(self.wpa_rankings)]
    
    def update_wpa_rankings(self, p_id : int, wpa_value):
        # Remove the old entry for this player if it exists
        self.wpa_rankings = [(p, w) for p, w in self.wpa_rankings if p != p_id]
        # Insert the new value in sorted order
        bisect.insort(self.wpa_rankings, (p_id, wpa_value), key=lambda x: x[1])
        # Check the min and max for scale range
        self.wpa_max = max(self.wpa_rankings, key=lambda x: x[1])[1]
        self.wpa_min = min(self.wpa_rankings, key=lambda x: x[1])[1]
        
        
        
    '''

            Node/Edge Creation Truth Table

            P1  |   P2  |   P3  |
            0   |   X   |   X   |   <-- No valid P1, means the other players don't matter
            1   |   1   |   X   |   <-- P2 linked, add edge(P1-P2) 
            1   |   0   |   0   |   <-- Only P1 needs to be updated
            1   |   0   |   1   |   <-- Blocks only, add edge(P3->P1)   

            
    '''
    
    def buildGraph(self, play_by_play_df):
        home_win_prob = 0.5
        for event in play_by_play_df.iter_rows():
            self.away_score = event[SCORE_AWAY_INDEX]
            self.home_score = event[SCORE_HOME_INDEX]    
            if (action := event[PLAY_ACTION_INDEX]) == -1:
                continue
            
            home_event = False
            
            # Inference columns for win prob: [PERIOD, PCTIMESTRING, scoreHome, scoreAway, PLAY_ACTION, HOME_AWAY_BOOL]
            win_prob_row = [event[PERIOD_INDEX], event[PCTIMESTRING_INDEX], event[SCORE_HOME_INDEX], event[SCORE_AWAY_INDEX], event[PLAY_ACTION_INDEX]]
            if event[P1_TEAM_ID_INDEX] == self.home_team_id:
                win_prob_row.append(1)
                home_event = True
            else:
                win_prob_row.append(0)
             
            # predict_proba expects a 2d array, might as well convert to np here rather than sklearn call doing it
            win_prob_row_reshape = np.array(win_prob_row).reshape(1, -1)
            
            # predict home win probability after event (class of 1 is home_win)
            play_win_prob = self.wpa_model.predict_proba(win_prob_row_reshape)[0][1]
            
            # get change in win probability as win probability added (wpa)
            wpa = play_win_prob - home_win_prob
            wpa_abs = abs(wpa)
            
            # STL
            if action == 1:
                # P2 steals from P1
                from_player = players.find_player_by_id(player_id=event[P2_ID_INDEX])
                to_player = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                
                if from_player:
                    # player who got the steal
                    from_node = self.playerNodeGetOrAdd(
                        player_id=event[P2_ID_INDEX],
                        player_name=from_player.get("full_name"),
                        player_team_id=event[P2_TEAM_ID_INDEX],
                        player_display_name=from_player.get("last_name")
                    )
                    from_node.STL += 1
                    from_node.wpa_absolute += wpa_abs
                    
                    if home_event:
                        from_node.wpa_net -= wpa
                    else:
                        from_node.wpa_net += wpa

                    
                if to_player:
                    # player who got stolen from - i.e. turnover
                    to_node = self.playerNodeGetOrAdd(
                        player_id=event[P1_ID_INDEX],
                        player_name=to_player.get("full_name"),
                        player_team_id=event[P1_TEAM_ID_INDEX],
                        player_display_name=to_player.get("last_name")
                    )                   
                    to_node.TO += 1
                    to_node.wpa_absolute += wpa_abs
                                
                    if home_event:
                        to_node.wpa_net += wpa
                    else:
                        to_node.wpa_net -= wpa
                
                
                # update game_edge to reflect event
                if from_player and to_player:
                    game_edge = from_node.gameEdgeGetOrAdd(to_pid=event[P1_ID_INDEX], off_bool=False)
                    game_edge.updateStatsEdge(action_stat=action, wp_change=wpa_abs)
                        
            # BLK
            elif action == 2:
                # P3 blocks P1
                from_player = players.find_player_by_id(player_id=event[P3_ID_INDEX])
                to_player = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                
                if from_player:
                    # player who blocks
                    from_node = self.playerNodeGetOrAdd(
                        player_id=event[P3_ID_INDEX],
                        player_name=from_player.get("full_name"),
                        player_team_id=event[P3_TEAM_ID_INDEX],
                        player_display_name=from_player.get("last_name")
                    )
                    from_node.BLK += 1
                    from_node.wpa_absolute += wpa_abs
                    if home_event:
                        from_node.wpa_net -= wpa
                    else:
                        from_node.wpa_net += wpa
                    
                    
                if to_player:
                    # player who got blocked
                    to_node = self.playerNodeGetOrAdd(
                        player_id=event[P1_ID_INDEX],
                        player_name=to_player.get("full_name"),
                        player_team_id=event[P1_TEAM_ID_INDEX],
                        player_display_name=to_player.get("last_name")
                    )  
                
                    to_node.wpa_absolute += wpa_abs
                    if home_event:
                        to_node.wpa_net += wpa
                    else:
                        to_node.wpa_net -= wpa
                
                if from_player and to_player:
                    # update game_edge to reflect event
                    game_edge = from_node.gameEdgeGetOrAdd(to_pid=event[P1_ID_INDEX], off_bool=False)
                    game_edge.updateStatsEdge(action_stat=action, wp_change=wpa_abs)
                
            # MAKE
            elif action == 3:
                points = 2
                if (made_three_bool := re.search(r"3PT", event[DESCRIPTION_INDEX])):
                    points = 3
                
                scorer_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if scorer_data:
                    scorer_node = self.playerNodeGetOrAdd(
                        player_id=event[P1_ID_INDEX],
                        player_name=scorer_data.get("full_name"),
                        player_team_id=event[P1_TEAM_ID_INDEX],
                        player_display_name=scorer_data.get("last_name")
                    )        
                
                    scorer_node.PTS += points
                    scorer_node.wpa_absolute += wpa_abs
                    if home_event:
                        scorer_node.wpa_net += wpa
                    else:
                        scorer_node.wpa_net -= wpa
    
                
                if (P2_DATA := players.find_player_by_id(event[P2_ID_INDEX])) and (P2_DATA.get("is_active") == True):
                    assister_node = self.playerNodeGetOrAdd(
                        player_id=event[P2_ID_INDEX],
                        player_name=P2_DATA.get("full_name"),
                        player_team_id=event[P2_TEAM_ID_INDEX],
                        player_display_name=P2_DATA.get("last_name")
                    )
                    
                    # update assister's stats
                    assister_node.AST += 1
                    assister_node.wpa_absolute += wpa_abs
                    
                    if home_event:
                        assister_node.wpa_net += wpa
                    else:
                        assister_node.wpa_net -= wpa
                    
                    if scorer_data:
                        game_edge = assister_node.gameEdgeGetOrAdd(to_pid=event[P1_ID_INDEX], off_bool=True)
                        game_edge.updateStatsEdge(action_stat=action, wp_change=wpa_abs, three_made=made_three_bool)  
            
            # MISS
            elif action == 4:
                player_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if player_data:
                    player_node = self.playerNodeGetOrAdd(
                        player_id=event[P1_ID_INDEX],
                        player_name=player_data.get("full_name"),
                        player_team_id=event[P1_TEAM_ID_INDEX],
                        player_display_name=player_data.get("last_name")
                    )
                    player_node.wpa_absolute += wpa_abs
                    if home_event:
                        player_node.wpa_net += wpa
                    else:
                        player_node.wpa_net -= wpa
            
            # TURNOVER
            elif action == 5:
                player_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if not player_data:
                    continue
                player_node = self.playerNodeGetOrAdd(
                    player_id=event[P1_ID_INDEX],
                    player_name=player_data.get("full_name"),
                    player_team_id=event[P1_TEAM_ID_INDEX],
                    player_display_name=player_data.get("last_name")
                )
                
                # offensive foul marked as turnover, but need to attribute a foul to the player too
                if "FOUL" in event[SUB_TYPE_INDEX]:
                    player_node.TO += 1
                    player_node.PF += 1
                else:
                    player_node.TO += 1
                
                player_node.wpa_absolute += wpa_abs
                if home_event:
                    player_node.wpa_net += wpa
                else:
                    player_node.wpa_net -= wpa
            
            # FOUL
            elif action == 6:
                # P1 fouls P2
                from_player = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                to_player = players.find_player_by_id(player_id=event[P2_ID_INDEX])
                if from_player:
                    # player who fouls
                    from_node = self.playerNodeGetOrAdd(
                        player_id=event[P1_ID_INDEX],
                        player_name=from_player.get("full_name"),
                        player_team_id=event[P1_TEAM_ID_INDEX],
                        player_display_name=from_player.get("last_name")
                    )
                    from_node.PF += 1
                    from_node.wpa_absolute += wpa_abs
                    if home_event:
                        from_node.wpa_net -= wpa
                    else:
                        from_node.wpa_net += wpa

                
                if to_player:
                # player who got fouled
                    to_node = self.playerNodeGetOrAdd(
                        player_id=event[P2_ID_INDEX],
                        player_name=to_player.get("full_name"),
                        player_team_id=event[P2_TEAM_ID_INDEX],
                        player_display_name=to_player.get("last_name")
                    )  
                    to_node.F_DRAWN += 1
                    # update player wpa
                    to_node.wpa_absolute += wpa_abs                    
                    if home_event:
                        to_node.wpa_net += wpa
                    else:
                        to_node.wpa_net -= wpa
                
                if from_player and to_player:
                    # update game_edge to reflect event
                    game_edge = from_node.gameEdgeGetOrAdd(to_pid=event[P2_ID_INDEX], off_bool=False)
                    game_edge.updateStatsEdge(action_stat=action, wp_change=wpa_abs)
            
            # FT_MAKE
            elif action == 8:
                player_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if not player_data:
                    continue
                player_node = self.playerNodeGetOrAdd(
                    player_id=event[P1_ID_INDEX],
                    player_name=player_data.get("full_name"),
                    player_team_id=event[P1_TEAM_ID_INDEX],
                    player_display_name=player_data.get("last_name")
                )
                player_node.PTS += 1
                
                player_node.wpa_absolute += wpa_abs
                if home_event:
                    player_node.wpa_net += wpa
                else:
                    player_node.wpa_net -= wpa
                
                # if event[P1_ID_INDEX] == 1630162:   
                #     print(f"PLAYER: {player_data.get("full_name")}, DESC: {event[DESCRIPTION_INDEX]}, CURR_PTS: {player_node.PTS}")
            
            # FT_MISS
            elif action == 7:
                player_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if not player_data:
                    continue
                player_node = self.playerNodeGetOrAdd(
                    player_id=event[P1_ID_INDEX],
                    player_name=player_data.get("full_name"),
                    player_team_id=event[P1_TEAM_ID_INDEX],
                    player_display_name=player_data.get("last_name")
                )
                
                player_node.wpa_absolute += wpa_abs
                if home_event:
                    player_node.wpa_net += wpa
                else:
                    player_node.wpa_net -= wpa

            # REB
            elif action == 9:
                player_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if not player_data:
                    continue
                player_node = self.playerNodeGetOrAdd(
                    player_id=event[P1_ID_INDEX],
                    player_name=player_data.get("full_name"),
                    player_team_id=event[P1_TEAM_ID_INDEX],
                    player_display_name=player_data.get("last_name")
                )
                player_node.REB += 1
                
                player_node.wpa_absolute += wpa_abs
                if home_event:
                    player_node.wpa_net += wpa
                else:
                    player_node.wpa_net -= wpa

            # TECH_FOUL
            elif action == 10:
                player_data = players.find_player_by_id(player_id=event[P1_ID_INDEX])
                if not player_data:
                    continue
                player_node = self.playerNodeGetOrAdd(
                    player_id=event[P1_ID_INDEX],
                    player_name=player_data.get("full_name"),
                    player_team_id=event[P1_TEAM_ID_INDEX],
                    player_display_name=player_data.get("last_name")
                )                
                player_node.F_TECH += 1
                
                player_node.wpa_absolute += wpa_abs
                if home_event:
                    player_node.wpa_net += wpa
                else:
                    player_node.wpa_net -= wpa

            # Update rankings for P1
            if event[P1_ID_INDEX] and event[P1_ID_INDEX] in self.graph_nodes:
                p1_node = self.graph_nodes.get(event[P1_ID_INDEX])
                self.update_wpa_rankings(event[P1_ID_INDEX], p1_node.wpa_absolute)
            
            # Update rankings for P2 if involved
            if event[P2_ID_INDEX] and event[P2_ID_INDEX] in self.graph_nodes:
                p2_node = self.graph_nodes[event[P2_ID_INDEX]]
                self.update_wpa_rankings(event[P2_ID_INDEX], p2_node.wpa_absolute)
            
            # Update rankings for P3 if involved
            if event[P3_ID_INDEX] and event[P3_ID_INDEX] in self.graph_nodes:
                p3_node = self.graph_nodes[event[P3_ID_INDEX]]
                self.update_wpa_rankings(event[P3_ID_INDEX], p3_node.wpa_absolute)

        
    def playerNodeGetOrAdd(self, player_id, player_name, player_team_id, player_display_name):
        return self.graph_nodes.setdefault(player_id, playerNode(id=player_id, full_name=player_name, team_id=player_team_id, display_name=player_display_name))
    
    def getCytoScapeElementList(self):   
        
        elements = []
        base_size = 60
        
        
        for id, player in self.graph_nodes.items():
            wpa_ratio = player.wpa_absolute / self.wpa_max
            adjusted_node_size = base_size + (wpa_ratio * 200)
            
            # add details for node itself
            elements.append({
                "data" : {
                    "id" : str(id), 
                    "label" : player.full_name,
                    "jersey_number" :  jersey_numbers_dict.get(str(id), "NR"),
                    "number_size" : (0.7 * adjusted_node_size),
                    "team" : player.team_id,
                    "node_size" : adjusted_node_size,
                    "home_away" : 1 if str(player.team_id) == self.home_team_id else 0
                    
                },
            })
            
            # add last name for self-loop for second node label
            elements.append({
                "data" : {
                    "source" : str(id),
                    "target" : str(id),
                    "display_edge" : str(True),
                    "display_name" : player.display_name,
                    "edge_distance" : max(adjusted_node_size / 2.1, 50)
                }
            })
            
            for edge_id, edge in player.connections.items():
                elements.append({
                    "data" : {
                        "source" : str(id), 
                        "target" : str(edge_id), 
                        "offense" : str(edge.offense),
                        "edge_stats" : edge.getEdgeStats(),
                    }
                })
                
        return elements
        
    # method to create json dump for dcc.Store, will later be used with from_json for full graph state mgmt        
    def to_json(self):
        graph_dict = {
            "game_id" : self.game_id,
            "home_id" : self.home_team_id,
            "away_id" : self.away_team_id,
            "home_score" : self.home_score,
            "away_score" : self.away_score,
            
            # serialize each player
            "nodes" : {
                str(p_id) : {
                    "id" : node.id,
                    "full_name" : node.full_name,
                    "team_id" : node.team_id,
                    "stats" : node.getPlayerStats(),
                    "game_edges" : {
                        str(to_pid) : edge.getEdgeStats() for to_pid, edge in node.connections.items()
                    }
                } for p_id, node in self.graph_nodes.items()
            }
        }        
        return json.dumps(graph_dict, indent=4)


# Main entry point for creating a game_graph
def buildGameGraph(game_id, home_team_id, away_team_id):
    
    # generate df for event iteration below
    play_by_play_df = utils.dfPolarsTest(game_id)
    # initialize the graph object using params
    game_graph = gameGraphBase(game_id=game_id, home_team_id=home_team_id, away_team_id=away_team_id)
    # build graph
    game_graph.buildGraph(play_by_play_df=play_by_play_df)
    return game_graph
    

