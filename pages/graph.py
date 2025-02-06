import math
import dash
from dash import Dash, html, dcc, Output, Input, callback, State
import dash_cytoscape as cyto
from graph_objects import gameGraphModels

dash.register_page(__name__, path='/graph')


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
                    'grabbable' : False
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

layout = html.Div([
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-5',
            elements=[],
            style={'width': '100%', 'height': '100vh'},
            layout={
                'fit' : True,
                'name': 'circle',
                'radius': 50,
                # 'startAngle': math.pi * -3 / 6,
                # 'sweep': math.pi * 6 / 6
            },
            # zoomingEnabled=True,
            stylesheet=default_cyto_stylesheet,
        ),

        html.Div(
            id='side-panel',
            style={
                'width': '300px',
                'height': '100%',
                'position': 'absolute',
                'right': '0',
                'top': '0',
                'backgroundColor': '#f8f9fa',
                'padding': '20px',
                'borderLeft': '1px solid #dee2e6',
                'display': 'none'
            },
            children=[
                html.H3("Player Details", style={'marginBottom': '20px'}),
                html.Div(id='node-stats-div')
            ]
        )
    ], style={'position': 'relative'}),
    
    # Stores elements of current graph
    dcc.Store(id="graph-elements-store", storage_type="session", data=None),
    
    # Stores which node is selected
    dcc.Store(id="selected-node-id", data=None)
])

@callback(
    [
        Output('side-panel', 'style'),
        Output('node-stats-div', 'children'),
        Output('cytoscape-layout-5', 'stylesheet'),
        Output('selected-node-id', 'data')
    ],
    Input('cytoscape-layout-5', 'tapNode'),
    State('selected-node-id' , 'data'),
    prevent_initial_call=True
)
def update_side_panel(node, selected_node):
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
                "opacity" : 0.2
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
    
    for edge in node['edgesData']:
        if edge['offense'] == "True":
            connection_color = "blue"
        else:
            connection_color = "red"
            
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
    
    player_stats = 0
    player = game_graph.graph_nodes.get(int(node['data']['id']), 0)
    if isinstance(player, gameGraphModels.playerNode):
        player_stats = player.getPlayerStats()
    return panel_style, f"Selected Player: {player_stats} ; {player}", stylesheet, node['data']['id']

@callback(
    Output("graph-elements-store", "data"),
    Input("selected-game-details", "data")
)
def createGraphFromSelection(game_details):
    if not game_details:
        return dash.no_update
    
    # create game_graph from selected game
    g_id, h_id, a_id = game_details.get("GAME_ID"), game_details.get("HOME_TEAM_ID"), game_details.get("VISITOR_TEAM_ID")
    game_graph = gameGraphModels.buildGameGraph(game_id=g_id, home_team_id=h_id, away_team_id=a_id)
    cytoscape_eles = game_graph.getCytoScapeElementList()
    
    # store created elements
    # TODO: need to add future ability to store full graph object to get stats as well
    return cytoscape_eles

@callback(
    Output("cytoscape-layout-5", "elements"),
    Input("graph-elements-store", "data")
)
def getStoredCytoElements(stored_elements):
    if not stored_elements:
        return dash.no_update
    
    return stored_elements