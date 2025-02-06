import dash
from dash import Dash, html, dcc, page_container, page_registry
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([ 
    dbc.NavbarSimple(
        brand="NavbarSimple",
        brand_href="/",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Graph", href="/graph", active=True))
        ],
    ),
    dcc.Store(id="selected-game-details", storage_type="session", data=None),
    page_container
])


if __name__ == '__main__':
    app.run(debug=True)