import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, State, dcc, html
from dash.dependencies import Input, Output

from newsfeed.get_summaries import get_summaries
from newsfeed.main import app


# Create a function to generate a card component for a summary
def generate_card(summary):
    return dbc.Card(
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
        )
    )


# The actual layout for the dash app
def create_layout(app: Dash) -> dbc.CardBody:
    # Get initial summaries based on the default value "tech"
    initial_summaries = get_summaries("tech")

    layout = dbc.Container(
        [
            daq.ToggleSwitch(
                label="Toggle switch", labelPosition="bottom", id="my_input", value="tech"
            ),
            html.Div(  # Container for card components
                id="summary-container",
                children=[generate_card(summary) for summary in initial_summaries],
            ),
        ],
        fluid=True,
    )

    return layout


@app.callback(
    Output("summary-container", "children"),  # Output: summary container's children
    Input("my_input", "value"),  # Input: toggle switch value
)
def update_summaries(value: str):
    summaries = get_summaries(value)
    return [generate_card(summary) for summary in summaries]
