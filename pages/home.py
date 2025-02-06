import dash
from dash import html, dcc, Input, Output, callback
from datetime import date

dash.register_page(__name__, path='/')

layout = html.Div([
    dcc.DatePickerSingle(
        id='game-search-date-entry',
        min_date_allowed=date(2023, 1, 1),
        max_date_allowed=date.today(),
        placeholder="Find Games by Date",
        display_format="MMMM DO, YYYY"
    ),
    html.Div('This is our Home page content.'),
])

