import dash
from dash import html, dcc, Input, Output, State, callback, dash_table
from datetime import date
from graph_objects import utils

dash.register_page(__name__, path='/')

layout = html.Div([
    dcc.DatePickerSingle(
        id='game-search-date-entry',
        min_date_allowed=date(2023, 1, 1),
        max_date_allowed=date.today(),
        placeholder="Find Games by Date",
        display_format="MMMM DO, YYYY"
    ),
    html.Div(id="game-date-results"),
])

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