import dash_bootstrap_components as dbc
from dash import Dash, html
from get_summaries import get_summaries


# The actual layout for the dash app
def create_layout(app: Dash) -> dbc.CardBody:
    summaries = get_summaries()

    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            # Use list comprehension to loop over all articles and create cards for each
                            dbc.CardBody(
                                [
                                    html.H4(summary.title, className="card-title"),
                                    html.P(summary.summary),
                                    html.P(
                                        f"Published: {summary.published}",
                                        style={"font-size": "12px", "color": "gray"},
                                    ),
                                    dbc.Button(
                                        "Visit Blog",
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
