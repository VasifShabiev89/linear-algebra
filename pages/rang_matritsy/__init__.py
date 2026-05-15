"""Topic: matrix rank — columns, span, dimensions."""

from __future__ import annotations

import dash
from dash import Input, Output, callback, callback_context, dcc, html

from dash_ui import (
    BTN,
    BTN_ROW,
    EXPLAIN,
    SECTION,
    STEP_LABEL,
    STEP_RADIO,
    back_link,
    graph_panel,
    section_title,
    shell,
)
from i18n import get_steps, normalize_locale, preset_hint, preset_label, step_count, t
from i18n.catalog import PRESET_IDS

from .viz_interactive import MATRIX_PRESETS, PRESET_ORDER, TOPIC, make_formula_step_figure

TOPIC_ID = TOPIC
STEP_N = step_count(TOPIC_ID)


def _step_options(lang: str) -> list[dict]:
    return [
        {"label": html.Span(s["title"], style=STEP_LABEL), "value": int(s["id"])}
        for s in get_steps(TOPIC_ID, lang)
    ]


def _preset_options(lang: str) -> list[dict]:
    return [
        {"label": preset_label(TOPIC_ID, pid, lang), "value": pid}
        for pid in PRESET_IDS[TOPIC_ID]
    ]


def _sidebar_i18n(lang: str) -> tuple:
    return (
        t("nav.back", lang),
        t("rang.page_title", lang),
        section_title(t("section.matrix", lang)),
        _preset_options(lang),
        section_title(t("section.step", lang)),
        _step_options(lang),
        t("nav.btn_prev", lang),
        t("nav.btn_next", lang),
        section_title(t("section.explanation", lang)),
    )


sidebar = [
    back_link("rank-back"),
    html.H2(
        id="rank-title",
        children="Matrix rank",
        style={"margin": "0 0 0.15rem", "fontSize": "1.15rem", "color": "#18181b"},
    ),
    html.P(
        html.Code("rank(A) = dim Col(A)", style={"fontSize": "0.8rem"}),
        style={"margin": "0 0 0.5rem", "color": "#52525b", "lineHeight": 1.4},
    ),
    html.Div(id="rank-sec-matrix", children=section_title("Matrix")),
    html.Div(
        dcc.Dropdown(
            id="rank-preset",
            options=_preset_options("en"),
            value=PRESET_ORDER[0],
            clearable=False,
        ),
        style=SECTION,
    ),
    html.Div(
        id="rank-preset-hint",
        style={"fontSize": "0.75rem", "color": "#71717a", "marginTop": "0.25rem"},
    ),
    html.Div(id="rank-sec-step", children=section_title("Step")),
    html.Div(
        dcc.RadioItems(
            id="rank-step",
            options=_step_options("en"),
            value=0,
            style=STEP_RADIO,
            inputStyle={"marginRight": "0.5rem"},
            labelStyle=STEP_LABEL,
        ),
        style=SECTION,
    ),
    html.Div(
        [
            html.Button("← Back", id="rank-btn-prev", n_clicks=0, style=BTN),
            html.Button("Next →", id="rank-btn-next", n_clicks=0, style=BTN),
        ],
        style=BTN_ROW,
    ),
    html.Div(
        id="rank-step-label",
        style={"fontSize": "0.78rem", "color": "#0F6E56", "marginTop": "0.35rem"},
    ),
    html.Div(id="rank-sec-explain", children=section_title("Explanation")),
    html.Div(id="rank-explain", style=EXPLAIN),
]

layout = shell(sidebar, [graph_panel("rank-graph")])


def _clamp_step(step: int) -> int:
    return max(0, min(step, STEP_N - 1))


@callback(
    Output("rank-graph", "figure"),
    Output("rank-explain", "children"),
    Output("rank-step", "value"),
    Output("rank-step-label", "children"),
    Output("rank-preset-hint", "children"),
    Output("rank-back", "children"),
    Output("rank-title", "children"),
    Output("rank-sec-matrix", "children"),
    Output("rank-preset", "options"),
    Output("rank-sec-step", "children"),
    Output("rank-step", "options"),
    Output("rank-btn-prev", "children"),
    Output("rank-btn-next", "children"),
    Output("rank-sec-explain", "children"),
    Input("locale", "data"),
    Input("rank-preset", "value"),
    Input("rank-step", "value"),
    Input("rank-btn-prev", "n_clicks"),
    Input("rank-btn-next", "n_clicks"),
)
def update_rank(
    locale: str | None,
    preset_name: str,
    step: int,
    _prev: int,
    _next: int,
):
    lang = normalize_locale(locale)
    i18n = _sidebar_i18n(lang)

    if preset_name not in MATRIX_PRESETS:
        preset_name = PRESET_ORDER[0]

    A = MATRIX_PRESETS[preset_name]
    hint = preset_hint(TOPIC_ID, preset_name, lang)
    step = _clamp_step(int(step if step is not None else 0))

    triggered = callback_context.triggered
    if triggered:
        prop = triggered[0]["prop_id"]
        if prop == "rank-btn-prev.n_clicks":
            step = _clamp_step(step - 1)
        elif prop == "rank-btn-next.n_clicks":
            step = _clamp_step(step + 1)

    fig, explain = make_formula_step_figure(A, step, lang)
    steps = get_steps(TOPIC_ID, lang)
    label = steps[step]["title"]
    return (fig, explain, step, label, hint, *i18n)


dash.register_page(
    __name__,
    path="/rang",
    name="Matrix rank",
    order=3,
    layout=layout,
)
