"""Topic: matrix projector A(AᵀA)⁻¹Aᵀ — formula step by step."""

from __future__ import annotations

import dash
import numpy as np
from dash import Input, Output, callback, callback_context, dcc, html

from dash_ui import (
    BTN,
    BTN_ROW,
    EXPLAIN,
    LABEL,
    SECTION,
    STEP_LABEL,
    STEP_RADIO,
    back_link,
    graph_panel,
    section_title,
    shell,
)
from i18n import get_steps, normalize_locale, preset_label, step_count, t
from i18n.catalog import PRESET_IDS

from .viz_interactive import MATRIX_PRESETS, PRESET_ORDER, TOPIC, make_formula_step_figure

TOPIC_ID = TOPIC
STEP_N = step_count(TOPIC_ID)
_, v0 = MATRIX_PRESETS[PRESET_ORDER[0]]


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


sidebar = [
    back_link("proektor-back"),
    html.H2(
        id="proektor-title",
        children="Projector",
        style={"margin": "0 0 0.15rem", "fontSize": "1.15rem", "color": "#18181b"},
    ),
    html.P(
        html.Code("proj = A(AᵀA)⁻¹Aᵀv", style={"fontSize": "0.8rem"}),
        style={"margin": "0 0 0.5rem", "color": "#52525b", "lineHeight": 1.4},
    ),
    html.Div(id="proektor-sec-matrix", children=section_title("Matrix")),
    html.Div(
        dcc.Dropdown(
            id="proektor-preset",
            options=_preset_options("en"),
            value=PRESET_ORDER[0],
            clearable=False,
        ),
        style=SECTION,
    ),
    html.Div(id="proektor-sec-step", children=section_title("Step")),
    html.Div(
        dcc.RadioItems(
            id="proektor-step",
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
            html.Button("← Back", id="proektor-btn-prev", n_clicks=0, style=BTN),
            html.Button("Next →", id="proektor-btn-next", n_clicks=0, style=BTN),
        ],
        style=BTN_ROW,
    ),
    html.Div(
        id="proektor-step-label",
        style={"fontSize": "0.78rem", "color": "#0F6E56", "marginTop": "0.35rem"},
    ),
    html.Div(id="proektor-sec-v", children=section_title("Vector v")),
    html.Div(
        [
            html.Label("vₓ", style=LABEL),
            dcc.Slider(
                id="proektor-vx",
                min=-3,
                max=5,
                step=0.1,
                value=float(v0[0]),
                marks={-3: "-3", 0: "0", 5: "5"},
                tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(
        [
            html.Label("vᵧ", style=LABEL),
            dcc.Slider(
                id="proektor-vy",
                min=-3,
                max=5,
                step=0.1,
                value=float(v0[1]),
                marks={-3: "-3", 0: "0", 5: "5"},
                tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(
        [
            html.Label("v_z", style=LABEL),
            dcc.Slider(
                id="proektor-vz",
                min=-4,
                max=8,
                step=0.1,
                value=float(v0[2]),
                marks={-4: "-4", 0: "0", 8: "8"},
                tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(id="proektor-sec-explain", children=section_title("Explanation")),
    html.Div(id="proektor-explain", style=EXPLAIN),
]


layout = shell(sidebar, [graph_panel("proektor-graph")])


def _clamp_step(step: int) -> int:
    return max(0, min(step, STEP_N - 1))


def _sidebar_i18n(lang: str) -> tuple:
    return (
        t("nav.back", lang),
        t("proektor.page_title", lang),
        section_title(t("section.matrix", lang)),
        _preset_options(lang),
        section_title(t("section.step", lang)),
        _step_options(lang),
        t("nav.btn_prev", lang),
        t("nav.btn_next", lang),
        section_title(t("section.vector_v", lang)),
        section_title(t("section.explanation", lang)),
    )


@callback(
    Output("proektor-graph", "figure"),
    Output("proektor-explain", "children"),
    Output("proektor-step", "value"),
    Output("proektor-step-label", "children"),
    Output("proektor-vx", "value"),
    Output("proektor-vy", "value"),
    Output("proektor-vz", "value"),
    Output("proektor-back", "children"),
    Output("proektor-title", "children"),
    Output("proektor-sec-matrix", "children"),
    Output("proektor-preset", "options"),
    Output("proektor-sec-step", "children"),
    Output("proektor-step", "options"),
    Output("proektor-btn-prev", "children"),
    Output("proektor-btn-next", "children"),
    Output("proektor-sec-v", "children"),
    Output("proektor-sec-explain", "children"),
    Input("locale", "data"),
    Input("proektor-preset", "value"),
    Input("proektor-step", "value"),
    Input("proektor-vx", "value"),
    Input("proektor-vy", "value"),
    Input("proektor-vz", "value"),
    Input("proektor-btn-prev", "n_clicks"),
    Input("proektor-btn-next", "n_clicks"),
)
def update_proektor(
    locale: str | None,
    preset_name: str,
    step: int,
    vx: float,
    vy: float,
    vz: float,
    _prev: int,
    _next: int,
):
    lang = normalize_locale(locale)
    i18n = _sidebar_i18n(lang)

    if preset_name not in MATRIX_PRESETS:
        preset_name = PRESET_ORDER[0]

    A, default_v = MATRIX_PRESETS[preset_name]
    step = _clamp_step(int(step if step is not None else 0))

    triggered = callback_context.triggered
    if triggered:
        prop = triggered[0]["prop_id"]
        if prop == "proektor-btn-prev.n_clicks":
            step = _clamp_step(step - 1)
        elif prop == "proektor-btn-next.n_clicks":
            step = _clamp_step(step + 1)
        elif prop.startswith("proektor-preset."):
            vx, vy, vz = float(default_v[0]), float(default_v[1]), float(default_v[2])

    v = np.array([vx, vy, vz], dtype=float)
    fig, explain = make_formula_step_figure(A, v, step, lang)
    steps = get_steps(TOPIC_ID, lang)
    label = steps[step]["title"]
    return (
        fig,
        explain,
        step,
        label,
        vx,
        vy,
        vz,
        *i18n,
    )


dash.register_page(
    __name__,
    path="/proektor",
    name="Matrix projector",
    order=4,
    layout=layout,
)
