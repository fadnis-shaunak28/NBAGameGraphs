from dataclasses import dataclass, field
import nba_api.stats.endpoints as nba_stats
import nba_api.live.nba.endpoints as nba_live
from nba_api.stats.static import players, teams
import utilities

@dataclass
class gameEdge:
    # required attributes for init args
    from_id : int
    to_id : int
    offense : bool
    
    # default stats set to 0
    AST : int = 0
    AST_PTS : int = 0
    STL : int = 0
    BLK : int = 0
    TO : int = 0
    PF : int = 0
    TIME_ON_SHARED : int = 0
    
    
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
    APM : float = 0
    TIME_ON_SEC : int = 0
    connections : list[gameEdge] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.id) # hash on player ID for game

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
            p1, p2, p3 = False, False, False
            
            ACTION_STAT = utilities.scrapeActionType(action_type_str=event[ACTION_TYPE_INDEX], description_str=event[DESCRIPTION_INDEX])
            
            # CHECKING IF EVENT HAS PLAYERS 1-3
            # TODO: figure out better way to manage p1, p2, p3 checking
            
            if (P1_res := players.find_player_by_id(player_id=event[P1_ID_INDEX])) and ((P1_res.get("is_active")) == True):
                p1 = True
            
            if (P2_res := players.find_player_by_id(player_id=event[P2_ID_INDEX])) and ((P2_res.get("is_active")) == True):
                p2 = True

            if (P3_res := players.find_player_by_id(player_id=event[P3_ID_INDEX])) and ((P3_res.get("is_active")) == True):
                p3 = True
            
            print("Players for Round DONE\n")
            
            
            if p1:  #   checking if valid play
                if (P1_ID := P1_res.get("id")) not in self.graph_nodes:
                    # create node
                    self.addPlayerNode(player_id=P1_ID, player_name=P1_res.get("full_name"), player_team_id=event[P1_TEAM_ID_INDEX])
                    
                # node guaranteed to be in graph now
                                
                if p2:  #   checking if there is a valid secondary player, 111 isn't worth it so if there is a one, only process the second player
                    if (P2_ID := P2_res.get("id")) not in self.graph_nodes:
                        # create node
                        self.addPlayerNode(player_id=P2_ID, player_name=P2_res.get("full_name"), player_team_id=event[P2_TEAM_ID_INDEX])

                    # node guaranteed to be in graph now
                    # add edge to player node    
                    
                    
                elif p3:   #    if p2 is False, then we only need to check p3 now   
                    if (P3_ID := P3_res.get("id")) not in self.graph_nodes:
                        # add node
                        self.addPlayerNode(player_id=P3_ID, player_name=P3_res.get("full_name"), player_team_id=event[P3_TEAM_ID_INDEX])

                    # node guaranteed to be in graph now
                    # add edge to player node                    
                    
                
            # if not a valid player play then move on and ignore
            else:
                pass
        
    def addPlayerNode(self, player_id, player_name, player_team_id):
        new_node = playerNode(id=player_id, full_name=player_name, team_id=player_team_id)
        self.graph_nodes[player_id] = new_node
        



def buildGameGraph(game_id : str, home_team_id : str, away_team_id : str):
    
    # initialize the graph object using params
    game_graph = gameGraphBase(game_id=game_id, home_team_id=home_team_id, away_team_id=away_team_id)
    
    # generate df for event iteration below
    play_by_play_df = utilities.create_clean_PBP_df(game_id)
    game_graph.buildGraph(play_by_play_df=play_by_play_df)
    
    
        