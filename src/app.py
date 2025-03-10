import dash
from dash import Dash, html, dcc, Input, State, Output, callback
import dash_bootstrap_components as dbc
from datetime import date, datetime
import dash_cytoscape as cyto



import offcanvas
import graph
from cytoscape_styles import cytoscape_stylesheet

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([ 
    dcc.Store(id="selected-game-store", data=None),                   
    
    # TODO: Need to update site title on navbar
    dbc.Navbar(
        children=[
            dbc.Row(
                [
                    dbc.Col(html.H4("NBA Game Graphs", className="text-light ms-5")),
                    dbc.Col(
                        dbc.Button(
                            "Select Game",
                            id="game-selector-nav-button",
                            className="ms-auto"
                        ),
                        width="auto",
                        align="end"
                    )
                ],
                align="center",
                style={
                    'width' : '100%'
                }
            )
        ],
        color="dark",
        dark=True,
        style={'height': '60px'}
    ),
        
    # add offcanvas
    dbc.Offcanvas(
        children=[
            dbc.Container(
                children=[dcc.DatePickerSingle(
                    initial_visible_month=date.today(),
                    id='game-search-date-entry',
                    min_date_allowed=date(2023, 1, 1),
                    max_date_allowed=date.today(),
                    placeholder="Find Games by Date",
                    display_format="MMMM DD, YYYY",
                    className="mx-auto d-block",
                    style={
                        'width' : '100%'
                    }
                )],
                class_name="d-flex justify-content-center"
            ),
            dbc.Container(
                id="game-date-results"
            ),

        ],
        style={
          'background-color' : '#212529'  
        },
        id="game-selector-offcanvas",
        is_open=False,
        title="Select Game"
    ),
    
    # add graph layout (includes side_panel)
    html.Div([
        html.Div([
            dcc.Loading(
                children=[
                    cyto.Cytoscape(
                        id='cytoscape-layout-5',
                        elements=[],
                        style={
                            'width': '100%', 
                            'height': 'calc(100vh - 60px)',
                            'background-color': '#D2A05F',
                            'background-image': 'url("/assets/court_lines_transparent.png")',  # Transparent PNG
                            'background-fit': 'contain',  # Ensures the whole court is visible
                            'background-repeat': 'no-repeat',
                            'background-position': 'center center',
                            'background-blend-mode' : 'multiply'
                        },
                        layout={
                            'fit' : True,
                            'name': 'circle',
                            'radius': 50,
                            # 'startAngle': math.pi * -3 / 6,
                            # 'sweep': math.pi * 6 / 6
                        },
                        zoomingEnabled=True,
                        stylesheet=cytoscape_stylesheet,
                        responsive=True
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
                    ),
                    
                    html.Div(
                        id="scoreboard-refit-div"
                    ),
                ],
                delay_show=300,
                

            ),
            
            
        ], style={'position': 'relative', 'background-color' : '#808080', 'height' : 'calc(100vh - 60px)', 'overflow' : 'hidden'}),
        
        # Stores elements of current graph
        dcc.Store(id="graph-elements-store", storage_type="session", data=None),
        
        # Stores current graph's data for clicking on node
        dcc.Store(id="graph-data-store", storage_type="session", data=None),
        
        # Stores which node is selected
        dcc.Store(id="selected-node-id", data=None)
    ])

        
])



if __name__ == '__main__':
    app.run(debug=False)
    
    
