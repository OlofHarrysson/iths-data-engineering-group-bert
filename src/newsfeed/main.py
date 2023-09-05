import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, html

from newsfeed.get_cached_files import get_contents

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Article Summaries from main"


def main():
    app.layout = create_layout()
    return app


@app.callback(  # This is the callback that will update the article container depending on the toggle switch
    Output("article_container", "children"), Input("toggle_switch", "value")
)
def update_summary_container(
    toggle_switch,
):  # This function will be called when the toggle switch is toggled
    if toggle_switch:
        summaries = get_contents("tech_summaries")
    else:
        summaries = get_contents("nontech_summaries")

    cards = [  # This is the list of cards that will be displayed in the article container
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(summary.title),
                    html.P(summary.summary),
                    html.P(
                        f"Published: {summary.published}",
                        style={"font-size": "12px", "color": "gray"},
                    ),
                    html.P(
                        f"Type: Tech" if toggle_switch else f"Type: Non-tech",
                        style={"font-size": "12px", "color": "gray"},
                    ),
                    dbc.Button(
                        "Visit Blog",
                        color="primary",
                        href=summary.link,
                        target="_blank",
                    ),
                ]
            ),
            color="dark",
            inverse=True,
        )
        for summary in summaries
    ]
    return cards


def create_layout():  # This function creates the layout for the dash app
    return dbc.CardBody(
        [
            dbc.Row(dbc.Col(dbc.Card(html.H1("Newsfeed"), body=True, color="dark", inverse=True))),
            dbc.Row(
                dbc.Col(
                    daq.ToggleSwitch(
                        id="toggle_switch", value=False, color="#9B51E0", label=["Non-Tech", "Tech"]
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        id="article_container", width=12
                    )  # This is the container that will hold the articles and will be updated by the callback
                ]
            ),
        ]
    )


if __name__ == "__main__":
    app_instance = main()
    app_instance.run_server(debug=True)
