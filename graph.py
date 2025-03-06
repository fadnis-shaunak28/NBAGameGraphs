import math
import dash
from dash import Dash, html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from graph_objects import gameGraphModels
from cytoscape_styles import cytoscape_stylesheet, node_selected_stylesheet, team_colors_styles
import nba_api.stats.static.teams as teams_data
import sys
import json


@callback(
    [
        Output('side-panel', 'style'),
        Output('node-stats-div', 'children'),
        Output('cytoscape-layout-5', 'stylesheet'),
        Output('selected-node-id', 'data'),
    ],
    Input('cytoscape-layout-5', 'tapNode'),
    [
        State('selected-node-id' , 'data'),
        State('graph-data-store', "data")
    ],
    prevent_initial_call=True
)
def update_side_panel(node, selected_node, stored_graph_data):
    offense_edges = {}
    defense_edges = {}
    
    if not node:
        return {'display': 'none'}, "No node selected", cytoscape_stylesheet, None
    
    if selected_node == node['data']['id']:
        return {'display' : 'none'}, "", cytoscape_stylesheet, None
    
    # Default style for visible panel
    panel_style = {
        'width': '300px',
        'height': '100%',
        'position': 'absolute',
        'right': '0',
        'top': '0',
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'borderLeft': '1px solid #dee2e6',
        'display': 'block'
    }
    
    stylesheet = [
        {
            'selector': 'node',
            'style': {
                'label': 'data(jersey_number)',
                'font-family' : 'JERSEY_NUMBER_FONT',
                'font-size': "data(number_size)",
                'text-valign': 'center',
                'text-halign': 'center',
                'text-margin-y' : 'mapData(number_size, 42, 182, 5, 15)',
                'width': 'data(node_size)',
                'height': 'data(node_size)',
                # 'width': 100,
                # 'height': 100,
                'grabbable' : False,
                "border-color" : "#050505",
                "border-width" : 2,
                "background-color" : "white",
                "shape": 'polygon',
                'opacity' : 0.2,
                'shape-polygon-points': '-0.3 -1, -0.3 -0.85, 0 -0.7, 0.3 -0.85, 0.3 -1, 0.5 -1, 0.8 -0.4, 0.8 1, -0.8 1, -0.8 -0.4, -0.5 -1'

            }
        },
        
        {
            "selector" : 'edge[display_edge = "True"]' ,
            'style': {
                'label': 'data(display_name)',
                'font-family' : 'JERSEY_NUMBER_FONT',
                'font-size' : '30px',
                'line-opacity' : "0",
                'z-index' : 100,
                'loop-direction' : '-180deg',
                'loop-sweep' : '0deg',
                "control-point-step-size": 'data(edge_distance)',
                "text-opacity" : 0.2,
                # "text-halign": "center",
                # "text-valign": "top",
                # "text-margin-y": "data(node_size)",  # Dynamically move label down
                'text-border-color': 'white',  # Border color for the text
                'text-border-width': '2px',  # Border width around the text

            }
        },
        
        {
            "selector": "edge",
            "style": {
                "line-opacity": 0,
                "curve-style": "bezier",
            },
        },
    ]
    
    stylesheet.extend([
        {
            "selector": f'node[id = "{node["data"]["id"]}"]',
            "style": {
                "border-color": "green",
                "border-width": 10,
                "border-opacity": 1,
                "opacity": 1,
                "z-index": 9999,
            },
        },
        
        {
            "selector" : f'edge[display_edge = "True"][source = "{node["data"]["id"]}"][target = "{node["data"]["id"]}"]' ,
            'style': {
                "text-opacity" : 1,
            }
        }
    ])
    
    # get graph data to describe data in each row
    player_data = json.loads(stored_graph_data)['nodes']

    
    for edge in node['edgesData']:
        if edge.get('display_edge'):
            continue
        
        connection_color = "blue" if edge['offense'] == "True" else "red"
        is_outgoing = edge['source'] == node['data']['id']
        
        edge_div = html.Div(
            children=[html.P(f"{stat} : {value}") for stat, value in edge["edge_stats"].items()]
        )
        
        # outgoing from the selected player
        if edge['source'] == node['data']['id']:
            stylesheet.extend([
                {
                    'selector' : f'node[id = "{edge["target"]}"]',
                    'style' : {
                        'opacity' : 1
                    }  
                },
                
                {
                    "selector" : f'edge[display_edge = "True"][source = "{edge["target"]}"][target = "{edge["target"]}"]' ,
                    'style': {
                        "text-opacity" : 1,
                    } 
                },
                
                {
                    'selector': f'edge[id = "{edge["id"]}"]',
                    'style': {
                        'width': 8,
                        'line-opacity' : 1,
                        'line-color': connection_color,
                        'curve-style': 'bezier',
                        'source-arrow-color': connection_color,
                        'source-arrow-shape': 'triangle',
                    }
                }
            ])
            if edge['offense'] == 'True':
                off_edge = offense_edges.setdefault(edge['target'], {'incoming': None, 'outgoing': None})
                off_edge['incoming'] = edge_div
            else:
                def_edge = defense_edges.setdefault(edge['target'], {'incoming': None, 'outgoing': None})
                def_edge['incoming'] = edge_div

                
        # incoming to selected node
        elif edge['target'] == node['data']['id']:

            stylesheet.extend([
                {
                  'selector' : f'node[id="{edge["source"]}"]',
                  'style' : {
                      'opacity' : 1
                  }  
                },
                
                {
                    "selector" : f'edge[display_edge = "True"][source = "{edge["source"]}"][target = "{edge["source"]}"]' ,
                    'style': {
                        "text-opacity" : 1,
                    } 
                },
                
                {
                    'selector': f'edge[id = "{edge["id"]}"]',
                    'style': {
                        'width': 8,
                        'line-opacity' : 1,
                        'line-color': connection_color,
                        'curve-style': 'bezier',
                        'source-arrow-color': connection_color,
                        'source-arrow-shape': 'triangle',
                    }
                }
            ])
            
            if edge['offense'] == 'True':
                off_edge = offense_edges.setdefault(edge['source'], {'incoming': None, 'outgoing': None})
                off_edge['outgoing'] = edge_div

            else:
                def_edge = defense_edges.setdefault(edge['source'], {'incoming': None, 'outgoing': None})
                def_edge['outgoing'] = edge_div

            
            
            
    selected_player_data = player_data.get(node['data']['id'])
    


    player_panel_div = html.Div(
        children=[
            html.Div(
                children=[
                    html.H3(node["data"]["label"]),
                    html.P(f"Player Data: {selected_player_data.get("stats")}")
                ]
            ),
            
            html.H3("Offense Edges"),
            dbc.Accordion(
                children=[
                    dbc.AccordionItem(
                        children=[
                            html.P("Outgoing Edge:") if connection['outgoing'] else None,
                            connection['outgoing'],
                            html.P("Incoming Edge:") if connection['incoming'] else None,
                            connection['incoming']
                        ],
                        title=f"{player_data[player].get('full_name')}"
                    ) for player, connection in offense_edges.items()
                ],
                start_collapsed=True,
                flush=True
            ),
            html.H3("Defense Edges"),
            dbc.Accordion(
                children=[
                    dbc.AccordionItem(
                        children=[
                            html.P("Outgoing Edge:") if connection['outgoing'] else None,
                            connection['outgoing'],
                            html.P("Incoming Edge:") if connection['incoming'] else None,
                            connection['incoming']
                        ],
                        title=f"{player_data[player].get('full_name')}"
                    ) for player, connection in defense_edges.items()
                ],
                start_collapsed=True,
                flush=True
            )
        ]
    )
    stylesheet.extend(team_colors_styles)
    
    return panel_style, player_panel_div, stylesheet, node['data']['id']


@callback(
    [
        Output("cytoscape-layout-5", "elements"),
        Output("graph-elements-store", "data"),
        Output("graph-data-store", "data"),
        Output('home_abbr', 'children'),
        Output('home_score', 'children'),
        Output('away_score', 'children'),
        Output('away_abbr', 'children'),
    ],
    Input("selected-game-store", "data"),
    prevent_initial_call=True
)
def createGraphFromSelection(game_details):
    if not game_details:
        return dash.no_update, dash.no_update, dash.no_update, None, None, None, None
    
    # create game_graph from selected game
    g_id, h_id, a_id = game_details.get("GAME_ID"), game_details.get("HOME_TEAM_ID"), game_details.get("AWAY_TEAM_ID")
    game_graph = gameGraphModels.buildGameGraph(game_id=g_id, home_team_id=h_id, away_team_id=a_id)
    home_score, away_score = game_graph.home_score, game_graph.away_score
    h_abr = teams_data.find_team_name_by_id(h_id).get("abbreviation")
    a_abr = teams_data.find_team_name_by_id(a_id).get("abbreviation")
    home_abbr_div = html.H1(h_abr)
    away_abbr_div = html.H1(a_abr)
    home_score_div = html.H1(home_score)
    away_score_div = html.H1(away_score)
    
    
    cytoscape_eles = game_graph.getCytoScapeElementList()
    graph_data = game_graph.to_json()
    
    return cytoscape_eles, cytoscape_eles, graph_data, home_abbr_div, home_score_div, away_score_div, away_abbr_div


@callback(
    [
        Output("cytoscape-layout-5", "zoom"),
        Output("cytoscape-layout-5", "elements", {"allow_duplicate" : True}),
        Output("cytoscape-layout-5", "stylesheet", {"allow_duplicates" : True}),
        Output("side-panel", "style", {"allow_duplicates" : True}),
        Output("selected-node-id", "data", {"allow_duplicates" : True})
    ],
    Input("reset-cyto-btn", "n_clicks"),
    [
        State("graph-elements-store", "data")  # Use your stored elements
    ],
    prevent_initial_call=True
)
def resetCytoLayout(n_clicks, stored_elements):
    print(f"Reset button clicked {n_clicks} times")
    side_panel_style = {
        'width': '400px',
        'height': '100%',
        'position': 'absolute',
        'right': '0',
        'top': '0',
        'background-color': 'white',
        'padding': '20px',
        'borderLeft': '1px solid #dee2e6',
        'display': 'none',
        'overflow-y' : 'scroll'
    }
    return 1, stored_elements, cytoscape_stylesheet, side_panel_style, None