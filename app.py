import math

from dash import Dash, html
import dash_cytoscape as cyto
from graph_objects import gameGraphModels

app = Dash()

game_graph = gameGraphModels.buildGameGraph(game_id="0022400500", home_team_id="1", away_team_id="0")
elements = game_graph.getCytoScapeElementList()

app.layout = html.Div([
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
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 60,
                    'height': 60
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
                    'width': 2,
                    'line-color': '#666',
                    'line-style' : 'dashed',
                    'curve-style': 'bezier',
                    'arrow-shape': 'triangle'
                }
            },
            
            {
              "selector" : "edge[offense = 'True']"  ,
                'style': {
                    'width': 2,
                    'line-color': '#666',
                    'curve-style': 'bezier',
                    'arrow-shape': 'triangle'
                }
            },
            
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)