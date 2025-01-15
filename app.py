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
        zoomingEnabled=False
    )
])

if __name__ == '__main__':
    app.run(debug=True)