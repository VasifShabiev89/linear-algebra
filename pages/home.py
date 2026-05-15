"""Home screen — topic picker."""

from __future__ import annotations

import dash
from dash import Input, Output, callback, dcc, html

from dash_ui import ACCENT, FONT, HOME_GRID, HOME_INNER, HOME_PAGE, TOPIC_CARD
from i18n import normalize_locale, t
from topics import TOPICS

dash.register_page(__name__, path="/", name="Home", order=0)


def _topic_card(topic, lang: str) -> dcc.Link:
    tag = t(f"topic.{topic.id}.tag", lang) if topic.tag_key else None
    children: list = [
        html.Div(
            [
                html.Span(
                    tag,
                    style={
                        "fontSize": "0.65rem",
                        "fontWeight": 700,
                        "textTransform": "uppercase",
                        "letterSpacing": "0.06em",
                        "color": ACCENT,
                        "background": "#e8f3ef",
                        "padding": "0.2rem 0.45rem",
                        "borderRadius": "4px",
                    },
                )
                if tag
                else None,
                html.H3(
                    t(f"topic.{topic.id}.title", lang),
                    style={
                        "margin": "0.5rem 0 0.35rem",
                        "fontSize": "1.05rem",
                        "color": "#18181b",
                    },
                ),
                html.P(
                    t(f"topic.{topic.id}.subtitle", lang),
                    style={"margin": 0, "fontSize": "0.88rem", "color": "#52525b", "lineHeight": 1.45},
                ),
            ]
        ),
    ]
    if topic.formula:
        children.append(
            html.Code(
                topic.formula,
                style={
                    "display": "block",
                    "marginTop": "0.75rem",
                    "fontSize": "0.78rem",
                    "color": "#3f3f46",
                    "background": "#f4f4f5",
                    "padding": "0.4rem 0.55rem",
                    "borderRadius": "6px",
                },
            )
        )
    children.append(
        html.Span(
            t("home.open", lang),
            style={
                "display": "block",
                "marginTop": "0.85rem",
                "fontSize": "0.82rem",
                "fontWeight": 600,
                "color": ACCENT,
            },
        )
    )
    return dcc.Link(
        [c for c in children if c is not None],
        href=topic.path,
        className="topic-card",
        style=TOPIC_CARD,
    )


layout = html.Div(
    html.Div(
        [
            html.H1(
                id="home-h1",
                children="Linear algebra",
                style={
                    "margin": 0,
                    "fontSize": "2rem",
                    "fontWeight": 700,
                    "color": "#18181b",
                    "fontFamily": FONT,
                },
            ),
            html.P(
                id="home-subtitle",
                children="Interactive visualizations. Choose a topic:",
                style={"margin": "0.5rem 0 0", "fontSize": "1rem", "color": "#71717a"},
            ),
            html.Div(id="home-grid", style=HOME_GRID),
            html.P(
                id="home-footer",
                children="New topics will appear here as they are added.",
                style={"marginTop": "2rem", "fontSize": "0.8rem", "color": "#a1a1aa"},
            ),
        ],
        style=HOME_INNER,
    ),
    style=HOME_PAGE,
)


@callback(
    Output("home-h1", "children"),
    Output("home-subtitle", "children"),
    Output("home-grid", "children"),
    Output("home-footer", "children"),
    Input("locale", "data"),
)
def update_home(locale: str | None) -> tuple:
    lang = normalize_locale(locale)
    cards = [_topic_card(topic, lang) for topic in TOPICS]
    return (
        t("app.title", lang),
        t("home.subtitle", lang),
        cards,
        t("home.footer", lang),
    )
