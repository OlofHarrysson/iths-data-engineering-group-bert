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

    # return dbc.Card(
    #     dbc.CardBody(
    #         [
    #             html.H4("Card Title", className="card-title"),
    #             html.P("This is some example card content."),
    #             dbc.Button("Go somewhere", color="primary"),
    #         ],
    #         id="card-title"
    #     )
    # )
