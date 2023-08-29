from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html
from dash.dependencies import Input, Output
from dash.html import H1, H2, Button, Div, P

from newsfeed.dashboard.layout import create_layout

app = dash.Dash(__name__)  # Initialize the Dash app


def main() -> None:
    app.title = "Article Summaries from main"
    app.layout = create_layout(app)

    @app.callback(
        Output("card-title", "children"),  # Output: summary container's children
        Input("card-title", "children"),  # Input: summary container's children (not used here)
    )
    def update_summary_container(children):
        # You can perform data updates or calculations here if needed
        return children  # Return the unchanged children

    return app


# Run the app when the script is executed
if __name__ == "__main__":
    app_instance = main()
    app_instance.run_server(debug=True)  # Run the app in debug mode
