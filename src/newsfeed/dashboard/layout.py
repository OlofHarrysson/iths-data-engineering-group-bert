from dash import Dash, html

# Sample article data (replace this with your data)
articles = [
    {
        "title": "Article 1",
        "summary": "This is the summary of article 1.",
    },
    {
        "title": "Article 2",
        "summary": "This is the summary of article 2.",
    },
]


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        [
            # html.H1("Article Summaries"),
            # html.Hr(),
            html.Div(
                id="summary-container",
                children=[
                    # Generate a list of article summaries with read links
                    html.Div(
                        [
                            html.P(article["summary"], className="article-summary"),
                            html.A(
                                "Read full article", href=f"/article/{index}", className="read-link"
                            ),
                        ]
                    )
                    for index, article in enumerate(
                        articles
                    )  # Loop through articles and create summaries
                ],
            ),
        ]
    )
