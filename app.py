import math

from dash import Dash, html, dcc, Output, Input, callback
import dash_cytoscape as cyto
from graph_objects import gameGraphModels

app = Dash()

game_graph = gameGraphModels.buildGameGraph(game_id="0022400500", home_team_id="1", away_team_id="0")
elements = game_graph.getCytoScapeElementList()

default_cyto_stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 100,
                    'height': 100
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

app.layout = html.Div([
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-5',
            elements=elements,
            style={'width': '100%', 'height': '1200px'},
            layout={
                'name': 'circle',
                # 'radius': 250,
                # 'startAngle': math.pi * -3 / 6,
                # 'sweep': math.pi * 6 / 6
            },
            zoomingEnabled=False,
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
    ], style={'position': 'relative'})
])

@callback(
    [Output('side-panel', 'style'),
     Output('node-stats-div', 'children'),
     Output('cytoscape-layout-5', 'stylesheet')
     ],
    Input('cytoscape-layout-5', 'tapNode')
)
def update_side_panel(node):
    if not node:
        return {'display': 'none'}, "No node selected", default_cyto_stylesheet
    
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
                'width': 100,
                'height': 100,
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
        if edge['source'] == node['data']['id']:
            stylesheet.append(
            {
                'selector': f'node[id = "{edge["target"]}"]',
                'style': {
                    'background-color': "blue",
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 100,
                    'height': 100,
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
                        'line-color': 'blue',
                        'curve-style': 'bezier',
                        'source-arrow-color': 'blue',
                        'source-arrow-shape': 'triangle',
                    }
                }
            )

        elif edge['target'] == node['data']['id']:
            stylesheet.append(
                {
                    'selector': f'node[id = "{edge["source"]}"]',
                    'style': {
                        'background-color': "red",
                        'label': 'data(label)',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'width': 100,
                        'height': 100,
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
                        'line-color': 'red',
                        'curve-style': 'bezier',
                        'source-arrow-color': 'red',
                        'source-arrow-shape': 'triangle',
                    }
                }
            )
    
    player_stats = 0
    player = game_graph.graph_nodes.get(int(node['data']['id']), 0)
    if isinstance(player, gameGraphModels.playerNode):
        player_stats = player.getPlayerStats()
    return panel_style, f"Selected Player: {player_stats} ; {player}", stylesheet

if __name__ == '__main__':
    app.run(debug=True)