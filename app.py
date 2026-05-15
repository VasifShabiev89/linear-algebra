#!/usr/bin/env python3
"""
Single entry point: home menu and all topics.

Run:
    uv run python app.py

http://127.0.0.1:8050
"""

from __future__ import annotations

import dash
from dash import Dash, dcc, html

from dash_ui import init_app, language_switcher

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
init_app(app)

app.layout = html.Div(
    [
        dcc.Store(id="locale", data="en", storage_type="local"),
        language_switcher(),
        dcc.Location(id="url", refresh=False),
        dash.page_container,
    ]
)

# Dash auto-discovers pages/; importing home ensures home callbacks are registered
import pages.home  # noqa: E402, F401
import pages.proekcia_vektora_na_ploskost  # noqa: E402, F401
import pages.skaljarnoe_proizvedenie  # noqa: E402, F401
import pages.rang_matritsy  # noqa: E402, F401
import i18n.callbacks  # noqa: E402, F401

if __name__ == "__main__":
    print("Linear algebra: http://127.0.0.1:8050")
    print("Stop: Ctrl+C")
    app.run(debug=False, port=8050)
