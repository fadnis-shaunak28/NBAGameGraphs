import math
import dash
from dash import Dash, html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from graph_objects import gameGraphModels
import sys
import json


default_cyto_stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 'data(node_size)',
                    'height': 'data(node_size)',
                    # 'width': 100,
                    # 'height': 100,
                    'grabbable' : False,
                    "border-color" : "#050505",
                    "border-width" : 2,
                    "background-color" : "white",
                }
            },
            
            {
              "selector" : "node[team=1610612746]"  ,
                'style': {
                    'background-color' : '#0000ff'
                }
            },
            
            {
              "selector" : "node[team=1610612750]"  ,
                'style': {
                    'background-color' : '#ff0000'
                }
            },
            
                        {
              "selector" : "edge[offense = 'False']"  ,
                'style': {
                    'width': 5,
                    'line-color': '#red',
                    'line-style' : 'dashed',
                    'curve-style': 'bezier',
                    'source-arrow-color': 'red',
                    'source-arrow-shape': 'triangle',
                }
            },
            
            {
              "selector" : "edge[offense = 'True']"  ,
                'style': {
                    'width': 5,
                    'line-color': '#006400',
                    'curve-style': 'bezier',
                    'source-arrow-color': '#006400',
                    'source-arrow-shape': 'triangle',
                }
            },
            
]


@callback(
    [
        Output('side-panel', 'style'),
        Output('node-stats-div', 'children'),
        Output('cytoscape-layout-5', 'stylesheet'),
        Output('selected-node-id', 'data')
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
        return {'display': 'none'}, "No node selected", default_cyto_stylesheet, None
    
    if selected_node == node['data']['id']:
        return {'display' : 'none'}, "", default_cyto_stylesheet, None
    
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
            "selector": "node",
            "style" : {
                "opacity" : 0.2,
                "border-color": "#050505",
                "border-width" : 2,
                "background-color" : "white",
                'width': 'data(node_size)',
                'height': 'data(node_size)',
                
            }
        },
        {
            "selector": "edge",
            "style": {
                "opacity": 0,
                "curve-style": "bezier",
            },
        },
        {
            "selector": f'node[id = "{node["data"]["id"]}"]',
            "style": {
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'width': 'data(node_size)',
                'height': 'data(node_size)',
                "background-color": "#2CFF05",
                "border-color": "purple",
                "border-width": 2,
                "border-opacity": 1,
                "opacity": 1,
                "z-index": 9999,
            },
        },
    ]
    
    # get graph data to describe data in each row
    player_data = json.loads(stored_graph_data)['nodes']

    
    for edge in node['edgesData']:
        connection_color = "blue" if edge['offense'] == "True" else "red"
        is_outgoing = edge['source'] == node['data']['id']
        
        edge_div = html.Div(
            children=[html.P(f"{stat} : {value}") for stat, value in edge["edge_stats"].items()]
        )
            
        if edge['source'] == node['data']['id']:
            stylesheet.append(
            {
                
                'selector': f'node[id = "{edge["target"]}"]',
                'style': {
                    'background-color': connection_color,
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 'data(node_size)',
                    'height': 'data(node_size)',
                    'opacity': 0.7
                }
            }
            )
            stylesheet.append(
                {
                    'selector': f'edge[id = "{edge["id"]}"]',
                    'style': {
                        'width': 5,
                        'opacity' : 1,
                        'line-color': connection_color,
                        'curve-style': 'bezier',
                        'source-arrow-color': connection_color,
                        'source-arrow-shape': 'triangle',
                    }
                }
            )
            if edge['offense'] == 'True':
                off_edge = offense_edges.setdefault(edge['target'], {'incoming': None, 'outgoing': None})
                off_edge['incoming'] = edge_div
            else:
                def_edge = defense_edges.setdefault(edge['target'], {'incoming': None, 'outgoing': None})
                def_edge['incoming'] = edge_div

                

        elif edge['target'] == node['data']['id']:
            stylesheet.append(
                {
                    'selector': f'node[id = "{edge["source"]}"]',
                    'style': {
                        'background-color': connection_color,
                        'label': 'data(label)',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'width': 'data(node_size)',
                        'height': 'data(node_size)',
                        'opacity': 0.7
                    }
                }
            )
            stylesheet.append(
                {
                    'selector': f'edge[id = "{edge["id"]}"]',
                    'style': {
                        'width': 5,
                        'opacity' : 1,
                        'line-color': connection_color,
                        'curve-style': 'bezier',
                        'source-arrow-color': connection_color,
                        'source-arrow-shape': 'triangle',
                    }
                }
            )
            
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


    return panel_style, player_panel_div, stylesheet, node['data']['id']


@callback(
    [
        Output("cytoscape-layout-5", "elements"),
        Output("graph-elements-store", "data"),
        Output("graph-data-store", "data")
    ],
    Input("selected-game-store", "data"),
    prevent_initial_call=True
)
def createGraphFromSelection(game_details):
    if not game_details:
        return dash.no_update, dash.no_update, dash.no_update
    
    # create game_graph from selected game
    g_id, h_id, a_id = game_details.get("GAME_ID"), game_details.get("HOME_TEAM_ID"), game_details.get("VISITOR_TEAM_ID")
    game_graph = gameGraphModels.buildGameGraph(game_id=g_id, home_team_id=h_id, away_team_id=a_id)
    cytoscape_eles = game_graph.getCytoScapeElementList()
    graph_data = game_graph.to_json()
    
    # store created elements
    # TODO: need to add future ability to store full graph object to get stats as well
    return cytoscape_eles, cytoscape_eles, graph_data
