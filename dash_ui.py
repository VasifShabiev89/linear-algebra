"""Shared Dash styles and layout: menu, sidebar, graph."""

from __future__ import annotations

from dash import dcc, html

FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"
ACCENT = "#0F6E56"

ROOT = {
    "display": "flex",
    "height": "100vh",
    "width": "100vw",
    "margin": 0,
    "padding": 0,
    "fontFamily": FONT,
    "overflow": "hidden",
    "background": "#fff",
}

SIDEBAR = {
    "width": "300px",
    "minWidth": "280px",
    "maxWidth": "340px",
    "height": "100vh",
    "overflowY": "auto",
    "overflowX": "hidden",
    "padding": "1rem 1rem 1.5rem",
    "borderRight": "1px solid #e4e4e7",
    "background": "#f8f9fa",
    "boxSizing": "border-box",
    "flexShrink": 0,
}

MAIN = {
    "flex": "1",
    "height": "100vh",
    "minWidth": 0,
    "display": "flex",
    "flexDirection": "column",
    "background": "#fff",
}

GRAPH_WRAP = {
    "flex": "1",
    "minHeight": 0,
    "padding": "0.5rem 0.75rem 0.75rem 0",
}

GRAPH = {
    "height": "100%",
    "width": "100%",
}

LABEL = {
    "display": "block",
    "fontSize": "0.72rem",
    "fontWeight": 600,
    "textTransform": "uppercase",
    "letterSpacing": "0.04em",
    "color": "#71717a",
    "marginBottom": "0.35rem",
    "marginTop": "0.85rem",
}

SECTION = {
    "marginBottom": "0.25rem",
}

BTN_ROW = {
    "display": "flex",
    "gap": "0.4rem",
    "marginTop": "0.5rem",
}

BTN = {
    "flex": "1",
    "padding": "0.45rem 0.5rem",
    "fontSize": "0.82rem",
    "border": "1px solid #d4d4d8",
    "borderRadius": "6px",
    "background": "#fff",
    "cursor": "pointer",
}

EXPLAIN = {
    "fontFamily": "ui-monospace, 'SF Mono', Menlo, monospace",
    "fontSize": "0.78rem",
    "background": "#fff",
    "border": "1px solid #e4e4e7",
    "padding": "0.65rem 0.75rem",
    "borderRadius": "8px",
    "whiteSpace": "pre-wrap",
    "lineHeight": 1.5,
    "color": "#3f3f46",
    "maxHeight": "220px",
    "overflowY": "auto",
}

STEP_RADIO = {
    "display": "flex",
    "flexDirection": "column",
    "gap": "0.15rem",
}

STEP_LABEL = {
    "display": "block",
    "padding": "0rem 0.55rem",
    "fontSize": "0.8rem",
    "lineHeight": 1.3,
    "borderRadius": "6px",
    "cursor": "pointer",
    "border": "1px solid transparent",
}

HOME_PAGE = {
    "minHeight": "100vh",
    "overflowY": "auto",
    "background": "linear-gradient(160deg, #f4f7f5 0%, #ffffff 45%)",
    "padding": "2.5rem 1.5rem 3rem",
    "boxSizing": "border-box",
}

HOME_INNER = {
    "maxWidth": "920px",
    "margin": "0 auto",
}

HOME_GRID = {
    "display": "grid",
    "gridTemplateColumns": "repeat(auto-fill, minmax(280px, 1fr))",
    "gap": "1rem",
    "marginTop": "1.75rem",
}

TOPIC_CARD = {
    "display": "block",
    "padding": "1.15rem 1.25rem",
    "background": "#fff",
    "border": "1px solid #e4e4e7",
    "borderRadius": "12px",
    "textDecoration": "none",
    "color": "inherit",
    "boxShadow": "0 1px 2px rgba(0,0,0,0.04)",
    "transition": "border-color 0.15s, box-shadow 0.15s",
}

BACK_LINK = {
    "display": "inline-block",
    "fontSize": "0.8rem",
    "color": ACCENT,
    "textDecoration": "none",
    "marginBottom": "0.75rem",
    "fontWeight": 500,
}

GLOBAL_CSS = """
body { margin: 0; padding: 0; }
#react-entry-point, #react-entry-point > div { min-height: 100%; }
.dash-options-list-option { align-items: center; }
a.topic-card:hover {
    border-color: #0F6E56 !important;
    box-shadow: 0 4px 14px rgba(15, 110, 86, 0.12);
}
.locale-select-wrap .Select-control {
    border: 1px solid #d4d4d8 !important;
    border-radius: 6px !important;
    min-height: 32px !important;
}
.locale-select-wrap .Select-value-label {
    font-size: 0.82rem !important;
}
"""


def init_app(app) -> None:
    """Reset body margins for full-screen layout."""
    marker = "{%css%}"
    inject = f"{marker}<style>{GLOBAL_CSS}</style>"
    if marker in app.index_string and GLOBAL_CSS not in app.index_string:
        app.index_string = app.index_string.replace(marker, inject, 1)


def shell(sidebar: list, main: list) -> html.Div:
    return html.Div(
        [
            html.Div(sidebar, style=SIDEBAR),
            html.Div(main, style=MAIN),
        ],
        style=ROOT,
    )


def graph_panel(graph_id: str = "graph") -> html.Div:
    return html.Div(
        dcc.Graph(id=graph_id, style=GRAPH, config={"displayModeBar": True, "scrollZoom": True}),
        style=GRAPH_WRAP,
    )


def section_title(text: str) -> html.Div:
    return html.Div(
        text,
        style={
            "fontSize": "0.7rem",
            "fontWeight": 700,
            "textTransform": "uppercase",
            "letterSpacing": "0.06em",
            "color": ACCENT,
            "marginTop": "1rem",
            "marginBottom": "0.4rem",
            "paddingBottom": "0.25rem",
            "borderBottom": "1px solid #e4e4e7",
        },
    )


LANG_SELECT_WRAP = {
    "position": "fixed",
    "bottom": "0.75rem",
    "right": "0.75rem",
    "zIndex": 1000,
    "background": "rgba(255,255,255,0.94)",
    "border": "1px solid #e4e4e7",
    "borderRadius": "8px",
    "padding": "0.35rem 0.45rem",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
}

LANG_SELECT = {
    "width": "7.5rem",
    "fontSize": "0.82rem",
}


def language_switcher() -> html.Div:
    return html.Div(
        dcc.Dropdown(
            id="locale-select",
            options=[
                {"label": "English", "value": "en"},
                {"label": "Русский", "value": "ru"},
            ],
            value="en",
            clearable=False,
            style=LANG_SELECT,
        ),
        style=LANG_SELECT_WRAP,
        className="locale-select-wrap",
    )


def back_link(link_id: str = "back-link") -> dcc.Link:
    return dcc.Link("← All topics", id=link_id, href="/", style=BACK_LINK)


SCENE_UIREVISION = "3d-view"


def scene_3d(
    *,
    initial_eye: tuple[float, float, float] | None = None,
) -> dict:
    """Plotly 3D scene; omit camera on Dash updates so pan/zoom/rotate persist (uirevision)."""
    scene: dict = {
        "xaxis_title": "X",
        "yaxis_title": "Y",
        "zaxis_title": "Z",
        "aspectmode": "data",
        "uirevision": SCENE_UIREVISION,
    }
    if initial_eye is not None:
        scene["camera"] = {
            "eye": {"x": initial_eye[0], "y": initial_eye[1], "z": initial_eye[2]},
        }
    return scene
