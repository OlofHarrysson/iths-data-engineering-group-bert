from pathlib import Path

import dash
import dash_bootstrap_components as dbc

from newsfeed.layout import create_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Initialize the Dash app

# Run the app when the script is executed
if __name__ == "__main__":
    app.layout = create_layout(app)
    app.run_server(debug=True)  # Run the app in debug mode
