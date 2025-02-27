import dash
from dash import Dash, html, dcc, Input, State, Output, callback
import dash_bootstrap_components as dbc
from datetime import date, datetime
import dash_cytoscape as cyto



import offcanvas_test
import graph_test
from graph_test import default_cyto_stylesheet

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([ 
    dcc.Store(id="selected-game-store", data=None),                   
    
    dbc.NavbarSimple(
        brand="NBA Game Graphs",
        brand_href="/",
        color="dark",
        dark=True,
        children=[
            dbc.Button(
                "Select Game",
                id="game-selector-nav-button",
                className="ms-auto"
            )
        ],
    ),
    
    # add offcanvas
    dbc.Offcanvas(
        children=[
            dcc.DatePickerSingle(
                id='game-search-date-entry',
                min_date_allowed=date(2023, 1, 1),
                max_date_allowed=date.today(),
                placeholder="Find Games by Date",
                display_format="MMMM DO, YYYY",
                className="mx-auto d-block"
            ),
            dbc.Container(
                id="game-date-results"
            ),

        ],
        id="game-selector-offcanvas",
        is_open=False,
        title="Select Game"
    ),
    
    # add graph layout (includes side_panel)
    html.Div([
        html.Div([
            cyto.Cytoscape(
                id='cytoscape-layout-5',
                elements=[],
                style={
                    'width': '100%', 
                    'height': '100vh',
                    'background-color': '#dec3a0',
                },
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
                },
                children=[
                    html.H3("Player Details", style={'marginBottom': '20px'}),
                    html.Div(id='node-stats-div')
                ]
            )
        ], style={'position': 'relative'}),
        
        # Stores elements of current graph
        dcc.Store(id="graph-elements-store", storage_type="session", data=None),
        
        # Stores current graph's data for clicking on node
        dcc.Store(id="graph-data-store", storage_type="session", data=None),
        
        # Stores which node is selected
        dcc.Store(id="selected-node-id", data=None)
    ])

        
])





if __name__ == '__main__':
    app.run(debug=True)
    
    
