import dash
from dash import html, Input, State, Output, callback
import dash_bootstrap_components as dbc
from graph_objects import utils
import nba_api.stats.static.teams as teams_data

@callback(
    Output("game-selector-offcanvas", "is_open"),
    Input("game-selector-nav-button", "n_clicks"),
    [State("game-selector-offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output("game-date-results", "children"),
    Input("game-search-date-entry", "date")
)
def displayGamesByDate(selected_date):
    if selected_date is not None:
        games_dict = utils.getGamesByDate(selected_date)
        
        game_cards = []
        for game in games_dict:
            g_id, h_id, a_id = game.get("GAME_ID"), game.get("HOME_TEAM_ID"), game.get("VISITOR_TEAM_ID")
            h_abr = teams_data.find_team_name_by_id(h_id).get("abbreviation")
            a_abr = teams_data.find_team_name_by_id(a_id).get("abbreviation")
            game_card = dbc.Card(
                children=[
                    dbc.Button(
                        id={
                            'type' : 'game-search-card',
                            'g_id' : str(g_id),
                            'a_id' : str(a_id),
                            'h_id' : str(h_id)
                        },
                        children=[
                            dbc.Row(
                                [
                                dbc.Col(html.H3(h_abr)),
                                dbc.Col(html.P("VS")),
                                dbc.Col(html.H3(a_abr)),
                                ]
                            )
                        ]
                    )
                ]
            )
            game_cards.append(game_card)
            
        return html.Div(game_cards)
        
    else:
        return "Date Not Selected"
    
@callback(
    Output("selected-game-store", "data"),
    Input({"type" : "game-search-card", "g_id" : dash.ALL, "h_id" : dash.ALL, "a_id" : dash.ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def getSelectedGameDetails(selected_card):
    ctx = dash.ctx
    
    if not ctx.triggered:
        return "NO GAME SELECTED"
    
    clicked_game_details = {
            'GAME_ID' : ctx.triggered_id.get("g_id"),
            'HOME_TEAM_ID' : ctx.triggered_id.get("h_id"),
            'AWAY_TEAM_ID' : ctx.triggered_id.get("a_id")
        }
    
    return clicked_game_details