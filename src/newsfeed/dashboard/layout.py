import datetime

import dash_bootstrap_components as dbc
from dash import Dash, html

# Note the arguments maybe has to be changed for when the real data comes in.
# title: str
# summary: str
# link: str
# published: date


def create_layout(app: Dash) -> dbc.CardBody:
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(id="card-container"),
                html.Div(
                    [
                        html.H5("Article Summary", className="card-title"),
                        html.Hr(),
                        html.P(
                            "This is where the summary for the text shall be "
                            "This is where the summary for the text shall be"
                        ),
                        dbc.Button("Read full article", color="primary"),
                    ],
                    id="card-title",
                ),
            ]
        )
    )
