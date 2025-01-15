from dataclasses import dataclass, field
import nba_api.stats.endpoints as nba_stats
import nba_api.live.nba.endpoints as nba_live
from nba_api.stats.static import players, teams
from graph_objects import utils
from typing import Dict
import polars as pl
import re


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
    
    def __repr__(self):
        return f"Edge to {self.to_p_id}; Offense: {self.offense}"
    
    def __hash__(self):
        return hash(self.to_p_id)
    
    def updateStatsEdge(self, action_stat : str, **kwargs):
        if action_stat == "AST":
            self.AST += 1
            if kwargs.get("three_made", 0):
                self.AST_PTS += 3
            else:
                self.AST_PTS += 2
        elif action_stat == "STL":
            self.STL += 1
        elif action_stat == "BLK":
            self.BLK += 1
        elif action_stat == "PF":
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
            
        return stats
    
    
    
@dataclass
class playerNode:
    # required attributes for init args
    id : int
    full_name : str
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
    # APM : float = 0
    # TIME_ON_SEC : int = 0
    # ON_FLOOR : int = 0
    # ON_FLOOR_START : int = 0
    connections : Dict[str, gameEdge] = field(default_factory=dict)      # collection of edges out for a player, action is of form: this_player -> other_player
    LAST_UPDATED_EVENT : int = 0
    
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
        }
        
        return stats_dict
    

    def gameEdgeGetOrAdd(self, to_pid, off_bool : bool):
        game_edge = self.connections.setdefault(to_pid, gameEdge(to_p_id=to_pid, offense=off_bool))
        return game_edge
    
    def updateStatsNode(self, action_stat: str, event_num : int, **kwargs):        
        self.LAST_UPDATED_EVENT = event_num
        if action_stat == "TO":
            self.TO += 1
        elif action_stat == "AST":
            self.AST += 1
        elif action_stat == "BLK":
            self.BLK += 1
        elif action_stat == "STL":
            self.STL += 1
        elif action_stat == "PTS":
            if kwargs.get("three_made", False):
                self.PTS += 3
            else: 
                self.PTS += 2
        elif action_stat == "FT_MAKE":
            self.PTS += 1
        elif action_stat == "REB":
            self.REB += 1
        elif action_stat == "PF":
            self.PF += 1
        elif action_stat == "F_DRAWN":
            self.F_DRAWN += 1
        elif action_stat == "F_TECH":
            self.F_TECH += 1
        
                
            
class gameGraphBase:
    def __init__(self, game_id, home_team_id, away_team_id):
        self.game_id = game_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_score = 0
        self.away_score = 0
        
        self.graph_nodes = {}
        
        
    '''

            Node/Edge Creation Truth Table

            P1  |   P2  |   P3  |
            0   |   X   |   X   |   <-- No valid P1, means the other players don't matter
            1   |   1   |   X   |   <-- P2 linked, add edge(P1-P2) TODO: Add helper function for defining edge attribute and directionality
            1   |   0   |   0   |   <-- Only P1 needs to be updated
            1   |   0   |   1   |   <-- Blocks only, add edge(P3->P1)   


            TODO: Need to do NLP helper function to read the description to make changes
            
    '''
    
    def buildGraph(self, play_by_play_df):
        
        for event in play_by_play_df.iter_rows():    
            p1_exists, p2_exists, p3_exists = False, False, False
                                
            # CHECKING IF EVENT HAS PLAYERS 1-3
            # TODO: figure out better way to manage p1, p2, p3 checking
            
            if (P1_res := players.find_player_by_id(player_id=event[P1_ID_INDEX])) and ((P1_res.get("is_active")) == True):
                p1_exists = True
            
            if (P2_res := players.find_player_by_id(player_id=event[P2_ID_INDEX])) and ((P2_res.get("is_active")) == True):
                p2_exists = True

            if (P3_res := players.find_player_by_id(player_id=event[P3_ID_INDEX])) and ((P3_res.get("is_active")) == True):
                p3_exists = True
            
            missed_shot = True if re.search(pattern=r"MISS", string=event[DESCRIPTION_INDEX]) else False
            p1_action, p2_action, p3_action, play_direction = utils.scrapeActionType(action_type_str=event[ACTION_TYPE_INDEX], p1_bool=p1_exists, p2_bool=p2_exists, p3_bool=p3_exists, miss_bool=missed_shot)    

                    
            # if there is a P1 action then we need to update nodes
            if p1_action:
                made_three_bool = None
                p1_node = self.playerNodeGetOrAdd(player_id=event[P1_ID_INDEX], player_name=P1_res.get("full_name"), player_team_id=event[P1_TEAM_ID_INDEX])

                if re.search(r"3PT", event[DESCRIPTION_INDEX]):
                    made_three_bool = True                
                    p1_node.updateStatsNode(p1_action, event_num=event[EVENTNUM_INDEX], three_made=made_three_bool)
                else:
                    p1_node.updateStatsNode(p1_action, event_num=event[EVENTNUM_INDEX])
                
                
                #  print(f"EVENT: {event[EVENTNUM_INDEX]}, P1 : ANTHONY EDWARDS ({p1_action}), P2 : {p2_action}, P3 : {p3_action}, TO: {p1_node.TO}, CURRENT_PTS: {p1_node.PTS}\n DESCRIPTION: {event[DESCRIPTION_INDEX]} MADE_THREE_BOOL: {made_three_bool}\n")

                
                # Checking if p2/p3 are active secondary players
                offense_bool = True
                if p2_action:
                    if event[P2_TEAM_ID_INDEX] != event[P1_TEAM_ID_INDEX]:
                        offense_bool = False
                    # Need to update p2 stats so we get/add the node
                    p2_node = self.playerNodeGetOrAdd(player_id=event[P2_ID_INDEX], player_name=P2_res.get("full_name"), player_team_id=event[P2_TEAM_ID_INDEX])
                    p2_node.updateStatsNode(p2_action, event_num=event[EVENTNUM_INDEX])
                    
                    # Updating edge between two players, need to confirm play_direction
                    # print(f"P1: {p1_node.full_name} {p1_action} ; P2: {p2_node.full_name} {p2_action} ; OFFENSE {offense_bool}")
                    if not play_direction:
                        game_edge = p2_node.gameEdgeGetOrAdd(p1_node.id, off_bool=offense_bool)
                        if p2_action == "AST":
                            game_edge.updateStatsEdge(action_stat = p2_action, three_made=made_three_bool)
                    else:
                        game_edge = p1_node.gameEdgeGetOrAdd(p2_node.id, off_bool=offense_bool)
                        game_edge.updateStatsEdge(action_stat = p1_action)
                
                elif p3_action:
                    if event[P3_TEAM_ID_INDEX] != event[P1_TEAM_ID_INDEX]:
                        offense_bool = False
                    p3_node = self.playerNodeGetOrAdd(player_id=event[P3_ID_INDEX], player_name=P3_res.get("full_name"), player_team_id=event[P3_TEAM_ID_INDEX])
                    p3_node.updateStatsNode(p3_action, event_num=event[EVENTNUM_INDEX])
                
                    # print(f"P1: {p1_node.full_name} {p1_action} ; P3: {p3_node.full_name} {p3_action} ; OFFENSE {offense_bool}")

                    # Update/create edge between two players
                    game_edge = p3_node.gameEdgeGetOrAdd(p1_node.id, off_bool=offense_bool)
                    game_edge.updateStatsEdge(action_stat = p3_action)

                
        print("COMPLETED GRAPH")
        # return self.graph_nodes
                
        
    def playerNodeGetOrAdd(self, player_id, player_name, player_team_id):
        return self.graph_nodes.setdefault(player_id, playerNode(id=player_id, full_name=player_name, team_id=player_team_id))
    
    def getCytoScapeElementList(self):
        elements = []
        for id, player in self.graph_nodes.items():
            elements.append({
                "data" : {"id" : str(id), "label" : player.full_name},
            })
            for edge_id in player.connections:
                elements.append({"data" : {"source" : str(id), "target" : str(edge_id)}})
                
        return elements
                
        


def buildGameGraph(game_id : str, home_team_id : str, away_team_id : str):
    
    # initialize the graph object using params
    game_graph = gameGraphBase(game_id="0022400500", home_team_id=home_team_id, away_team_id=away_team_id)
    
    # generate df for event iteration below
    play_by_play_df = utils.create_clean_PBP_df(game_id)
    game_graph.buildGraph(play_by_play_df=play_by_play_df)
    return game_graph
    
        