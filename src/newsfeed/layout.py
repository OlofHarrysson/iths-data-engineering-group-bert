import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, html

from newsfeed.get_cached_files import get_contents


# The actual layout for the dash app
def create_layout(app: Dash) -> dbc.CardBody:
    tech_summaries = get_contents("tech_summaries")
    non_tech_summaries = get_contents("nontech_summaries")

    tech_cards = [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(summary.title, className="ccard-title"),
                    html.P(summary.summary),
                    html.P(
                        f"Published: {summary.published}",
                        style={"font-size": "12px", "color": "gray"},
                    ),
                    html.P(
                        f"Type: Tech",
                        style={"font-size": "12px", "color": "gray"},
                    ),
                    dbc.Button(
                        "Visit Blog",
                        color="primary",
                        href=summary.link,
                        target="_blank",
                    ),
                ]
            )
        )
        for summary in tech_summaries
    ]

    non_tech_cards = [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(summary.title, className="ccard-title"),
                    html.P(summary.summary),
                    html.P(
                        f"Published: {summary.published}",
                        style={"font-size": "12px", "color": "gray"},
                    ),
                    html.P(
                        f"Type: Nontech",
                        style={"font-size": "12px", "color": "gray"},
                    ),
                    dbc.Button(
                        "Visit Blog",
                        color="primary",
                        href=summary.link,
                        target="_blank",
                    ),
                ]
            )
        )
        for summary in non_tech_summaries
    ]

    return dbc.Row(
        [
            dbc.Col(tech_cards, style={"width": "40%", "inline-block": "True", "height": "100px"}),
            dbc.Col(
                non_tech_cards, style={"width": "40%", "inline-block": "True", "height": "100px"}
            ),
        ]
    )
