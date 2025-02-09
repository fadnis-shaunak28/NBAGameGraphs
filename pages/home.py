import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
from datetime import date
from graph_objects import utils

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.DatePickerSingle(
                id='game-search-date-entry',
                min_date_allowed=date(2023, 1, 1),
                max_date_allowed=date.today(),
                placeholder="Find Games by Date",
                display_format="MMMM DO, YYYY",
                className="mx-auto d-block"
            )
        ], width={"size": "auto"}, className="text-center my-4")
    ], justify="center"),
    html.Div(id="game-date-results", className="d-flex justify-content-center")
    
], fluid=True)

# TODO: Need to add styling to the table and also translate the Ids to 3-letter abbrev. and add logos
@callback(
    Output("game-date-results", "children"),
    Input("game-search-date-entry", "date")
)
def displayGamesByDate(selected_date):
    if selected_date is not None:
        
        games_dict = utils.getGamesByDate(selected_date)
        columns = [{"name": col, "id": col} for col in games_dict[0].keys()] if games_dict else []
        games_table = dash_table.DataTable(
            id="available-games-table",
            data=games_dict, 
            columns=columns,
            row_selectable='single'
        )
        return games_table
    else:
        return "Date Not Selected"
    
@callback(
    Output("selected-game-details", "data"),
    Input("available-games-table", "selected_rows"),
    State("available-games-table", "data")
)
def getSelectedGameDetails(selected_rows, table_data):
    if selected_rows:
        print(table_data[selected_rows[0]])
        return table_data[selected_rows[0]]
    else:
        return dash.no_update

# import dash
# from dash import html, dcc, Input, Output, State, callback, ALL
# import dash_bootstrap_components as dbc
# from datetime import date
# from graph_objects import utils
# import json

# dash.register_page(__name__, path='/')

# layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             dcc.DatePickerSingle(
#                 id='game-search-date-entry',
#                 min_date_allowed=date(2023, 1, 1),
#                 max_date_allowed=date.today(),
#                 placeholder="Find Games by Date",
#                 display_format="MMMM DO, YYYY",
#                 className="mx-auto d-block"
#             )
#         ], width={"size": "auto"}, className="text-center my-4")
#     ], justify="center"),
#     html.Div(id="game-date-results", className="d-flex justify-content-center")
    
# ], fluid=True)

# @callback(
#     Output("game-date-results", "children"),
#     Input("game-search-date-entry", "date")
# )
# def displayGamesByDate(selected_date):
#     if selected_date is not None:
#         games_dict = utils.getGamesByDate(selected_date)

#         games_list = [
#             dbc.Card(
#                 dbc.CardBody(
#                     dbc.Row([
#                         dbc.Col(html.Div(str(val)), width=4) for val in game.values()
#                     ] + [
#                         dbc.Col(
#                             dbc.Button(
#                                 "Select",
#                                 id={"type": "select-game-btn", "index": i},  # Button index
#                                 n_clicks=0,  # Default value
#                                 color="primary"
#                             ),
#                             width=2
#                         )
#                     ])
#                 ),
#                 className="mb-3"
#             ) for i, game in enumerate(games_dict)
#         ]

#         # Wrap in a parent container with game data as `data-*`
#         return html.Div(games_list, id="games-container", **{"data-games" : json.dumps(games_dict)})

#     else:
#         return "Date Not Selected"

# @callback(
#     Output("selected-game-details", "data"),
#     Input({"type": "select-game-btn", "index": ALL}, "n_clicks"),
#     State("games-container", "data-games"),  # Get the entire games list from the parent Div
#     prevent_initial_call=True
# )
# def getSelectedGameDetails(n_clicks, games_json):
#     ctx = dash.callback_context
#     if not ctx.triggered or not games_json:
#         return dash.no_update

#     # Load game data from the parent Div
#     games_dict = json.loads(games_json)

#     # Get which button was clicked
#     button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
#     index = button_id["index"]

#     # Return the full game dictionary for the selected card
#     return games_dict[index] if 0 <= index < len(games_dict) else dash.no_update