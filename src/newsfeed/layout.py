import datetime

import dash_bootstrap_components as dbc
from dash import Dash, html
from get_summaries import get_summaries

# Note the arguments maybe has to be changed for when the real data comes in.
# title: str
# summary: str
# link: str
# published: date


def create_layout(app: Dash) -> dbc.CardBody:
    summaries = get_summaries()

    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4(summary.title, className="card-title"),
                                    html.P(summary.summary),
                                    dbc.Button(
                                        "Go somewhere",
                                        color="primary",
                                        href=summary.link,
                                        target="_blank",
                                    ),
                                    html.P("Test", style={"font-size": "10px", "color": "gray"}),
                                ]
                            )  # ,
                            # id="card-title"
                        )
                        for summary in summaries  # Create 3 identical cards
                    ],
                    width=6,
                ),
            ),
        ],
        fluid=True,
    )
