# Importing packages/or modules
# H1 represents a top-level heading.
# H2 represents a secondary heading.
# P represents a paragraph.
# Div represents a generic division or container.
# Button represents a clickable button.
from pathlib import Path

import dash_bootstrap_components as dbc

# TODO: Clean the imports
from dash import Dash, Input, Output, State, dcc, html
from dash.html import H1, H2, Button, Div, P
from layout import create_layout


def main() -> None:
    app = Dash()
    app.title = "Dash App"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()
