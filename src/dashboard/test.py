# Import necessary modules from Dash
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample article data (replace this with your data)
articles = [
    {
        "title": "Article 1",
        "summary": "This is the summary of article 1.",
        "content": "This is the content of article 1. It's a very interesting article.",
    },
    {
        "title": "Article 2",
        "summary": "This is the summary of article 2.",
        "content": "This is the content of article 2. It's another exciting article.",
    },
]

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Article Summaries"),
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


# Define a callback function
@app.callback(
    Output("summary-container", "children"),  # Output: summary container's children
    Input("summary-container", "children"),  # Input: summary container's children (not used here)
)
def update_summary_container(children):
    # You can perform data updates or calculations here if needed
    return children  # Return the unchanged children


# Run the app when the script is executed
if __name__ == "__main__":
    app.run_server(debug=True)  # Run the app in debug mode
