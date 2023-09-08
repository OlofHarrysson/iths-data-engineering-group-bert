from urllib.parse import urlparse

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, html

from newsfeed.get_cached_files import get_contents

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
app.title = "Article Summaries from main"


def main():
    app.layout = create_layout()
    return app


@app.callback(  # This is the callback that will update the article container depending on the toggle switch
    Output("article_container", "children"),
    Input("switch_summary_type", "value"),
    Input("switch_language", "value"),
)
def update_summary_container(
    toggle_switch, language_switch
):  # This function will be called when the toggle switch is toggled
    language = "sv_" if language_switch else ""

    if toggle_switch:
        summaries = get_contents(f"{language}nontech_summaries")
    else:
        summaries = get_contents(f"{language}tech_summaries")

    summaries = amount_summaries_from_each_source(
        summaries, n=5
    )  # get top n most recent summaries from each unique source
    summaries = sort_summaries(summaries)  # sort summaries so last published appears at the top

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
                    dbc.Button(
                        f"Source: {get_source(summary)}",
                        color="primary",
                        href=summary.link,
                        target="_blank",
                    ),
                ]
            ),
            style={"margin-top": "10px"},
            color="dark",
            inverse=True,
        )
        for summary in summaries
    ]
    return cards


def sort_summaries(summaries):
    # sort summaries by published date in descending order (newest first)
    sorted_summaries = sorted(summaries, key=lambda x: x.published, reverse=True)

    return sorted_summaries


def get_source(summary):
    parsed_url = urlparse(summary.link)
    source = parsed_url.netloc  # netloc gives "https://example.com/something" -> "example.com"

    return source


def get_summary_by_source(summaries):
    summaries_dict = {}

    for summary in summaries:
        source = get_source(summary)

        if source not in summaries_dict:
            summaries_dict[source] = []

        summaries_dict[source].append(summary)

    return summaries_dict


def amount_summaries_from_each_source(summaries, n=10):
    top_summaries = []
    summaries_dict = get_summary_by_source(summaries)

    for source in summaries_dict:
        top_summaries.extend(summaries_dict[source][:n])

    return top_summaries


def create_layout():  # This function creates the layout for the dash app
    # title of the dashboard
    header = dbc.Row(
        [
            dbc.Col(
                html.H1("Newsfeed"),
                width={"size": 7, "offset": 1},
            ),
            dbc.Col(
                html.P(
                    f"Last Updated: [placeholder]",
                    style={"font-size": "12px", "color": "gray"},
                ),
                style={"text-align": "right", "vertical-align": "bottom"},
                width={"size": 3},
            ),
        ],
        style={"margin-top": "2%", "margin-bottom": "1%", "display": "flex"},
    )

    summary_type_toggle = html.Div(
        [
            dbc.RadioItems(
                id="switch_summary_type",  # this id updates if dashboard displays tech or nontech
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "Tech", "value": 0},
                    {"label": "Nontech", "value": 1},
                ],
                value=0,  # starting value (option that will be displayed by default)
            ),
        ],
        style={"margin-right": "1%"},
        className="radio-group",
    )

    language_toggle = html.Div(
        [
            dbc.RadioItems(
                id="switch_language",  # this id updates if dashboard displays english or swedish
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "English", "value": 0},
                    {"label": "Swedish", "value": 1},
                ],
                value=0,  # starting value (option that will be displayed by default)
            ),
        ],
        className="radio-group",
    )

    control_panel = dbc.Row(
        dbc.Col(
            [
                summary_type_toggle,
                language_toggle,
            ],
            style={"display": "flex"},
            width={"size": 10, "offset": 1},
        ),
    )

    # container holding all cards with summaries
    contents = dbc.Row(dbc.Col(id="article_container", width={"size": 10, "offset": 1}))

    return dbc.Container(
        [  # dbc.Card(html.H1("Newsfeed"), body=True, color="dark", inverse=True)
            header,
            control_panel,
            contents,
        ]
    )


if __name__ == "__main__":
    app_instance = main()
    app_instance.run_server(debug=True)
