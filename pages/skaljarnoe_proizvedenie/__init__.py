"""Topic: dot product — definition, angle, projection."""

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

from .viz_interactive import PRESET_ORDER, TOPIC, VECTOR_PRESETS, make_formula_step_figure

TOPIC_ID = TOPIC
STEP_N = step_count(TOPIC_ID)
a0, b0 = VECTOR_PRESETS[PRESET_ORDER[0]]


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
        t("skalyarnoe.page_title", lang),
        section_title(t("section.preset", lang)),
        _preset_options(lang),
        section_title(t("section.step", lang)),
        _step_options(lang),
        t("nav.btn_prev", lang),
        t("nav.btn_next", lang),
        section_title(t("section.vector_a", lang)),
        section_title(t("section.vector_b", lang)),
        section_title(t("section.explanation", lang)),
    )


sidebar = [
    back_link("scalar-back"),
    html.H2(
        id="scalar-title",
        children="Dot product",
        style={"margin": "0 0 0.15rem", "fontSize": "1.15rem", "color": "#18181b"},
    ),
    html.P(
        html.Code("a · b = |a||b|cos φ = a₁b₁ + …", style={"fontSize": "0.8rem"}),
        style={"margin": "0 0 0.5rem", "color": "#52525b", "lineHeight": 1.4},
    ),
    html.Div(id="scalar-sec-preset", children=section_title("Preset")),
    html.Div(
        dcc.Dropdown(
            id="scalar-preset",
            options=_preset_options("en"),
            value=PRESET_ORDER[0],
            clearable=False,
        ),
        style=SECTION,
    ),
    html.Div(id="scalar-sec-step", children=section_title("Step")),
    html.Div(
        dcc.RadioItems(
            id="scalar-step",
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
            html.Button("← Back", id="scalar-btn-prev", n_clicks=0, style=BTN),
            html.Button("Next →", id="scalar-btn-next", n_clicks=0, style=BTN),
        ],
        style=BTN_ROW,
    ),
    html.Div(
        id="scalar-step-label",
        style={"fontSize": "0.78rem", "color": "#0F6E56", "marginTop": "0.35rem"},
    ),
    html.Div(id="scalar-sec-a", children=section_title("Vector a")),
    html.Div(
        [
            html.Label("aₓ", style=LABEL),
            dcc.Slider(
                id="ax", min=-4, max=4, step=0.1, value=float(a0[0]),
                marks={-4: "-4", 0: "0", 4: "4"}, tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(
        [
            html.Label("aᵧ", style=LABEL),
            dcc.Slider(
                id="ay", min=-4, max=4, step=0.1, value=float(a0[1]),
                marks={-4: "-4", 0: "0", 4: "4"}, tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(
        [
            html.Label("a_z", style=LABEL),
            dcc.Slider(
                id="az", min=-4, max=4, step=0.1, value=float(a0[2]),
                marks={-4: "-4", 0: "0", 4: "4"}, tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(id="scalar-sec-b", children=section_title("Vector b")),
    html.Div(
        [
            html.Label("bₓ", style=LABEL),
            dcc.Slider(
                id="bx", min=-4, max=4, step=0.1, value=float(b0[0]),
                marks={-4: "-4", 0: "0", 4: "4"}, tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(
        [
            html.Label("bᵧ", style=LABEL),
            dcc.Slider(
                id="by", min=-4, max=4, step=0.1, value=float(b0[1]),
                marks={-4: "-4", 0: "0", 4: "4"}, tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(
        [
            html.Label("b_z", style=LABEL),
            dcc.Slider(
                id="bz", min=-4, max=4, step=0.1, value=float(b0[2]),
                marks={-4: "-4", 0: "0", 4: "4"}, tooltip={"placement": "bottom"},
            ),
        ],
        style=SECTION,
    ),
    html.Div(id="scalar-sec-explain", children=section_title("Explanation")),
    html.Div(id="scalar-explain", style=EXPLAIN),
]

layout = shell(sidebar, [graph_panel("scalar-graph")])


def _clamp_step(step: int) -> int:
    return max(0, min(step, STEP_N - 1))


@callback(
    Output("scalar-graph", "figure"),
    Output("scalar-explain", "children"),
    Output("scalar-step", "value"),
    Output("scalar-step-label", "children"),
    Output("ax", "value"),
    Output("ay", "value"),
    Output("az", "value"),
    Output("bx", "value"),
    Output("by", "value"),
    Output("bz", "value"),
    Output("scalar-back", "children"),
    Output("scalar-title", "children"),
    Output("scalar-sec-preset", "children"),
    Output("scalar-preset", "options"),
    Output("scalar-sec-step", "children"),
    Output("scalar-step", "options"),
    Output("scalar-btn-prev", "children"),
    Output("scalar-btn-next", "children"),
    Output("scalar-sec-a", "children"),
    Output("scalar-sec-b", "children"),
    Output("scalar-sec-explain", "children"),
    Input("locale", "data"),
    Input("scalar-preset", "value"),
    Input("scalar-step", "value"),
    Input("ax", "value"),
    Input("ay", "value"),
    Input("az", "value"),
    Input("bx", "value"),
    Input("by", "value"),
    Input("bz", "value"),
    Input("scalar-btn-prev", "n_clicks"),
    Input("scalar-btn-next", "n_clicks"),
)
def update_scalar(
    locale: str | None,
    preset_name: str,
    step: int,
    ax: float,
    ay: float,
    az: float,
    bx: float,
    by: float,
    bz: float,
    _prev: int,
    _next: int,
):
    lang = normalize_locale(locale)
    i18n = _sidebar_i18n(lang)

    if preset_name not in VECTOR_PRESETS:
        preset_name = PRESET_ORDER[0]

    default_a, default_b = VECTOR_PRESETS[preset_name]
    step = _clamp_step(int(step if step is not None else 0))

    triggered = callback_context.triggered
    if triggered:
        prop = triggered[0]["prop_id"]
        if prop == "scalar-btn-prev.n_clicks":
            step = _clamp_step(step - 1)
        elif prop == "scalar-btn-next.n_clicks":
            step = _clamp_step(step + 1)
        elif prop.startswith("scalar-preset."):
            ax, ay, az = float(default_a[0]), float(default_a[1]), float(default_a[2])
            bx, by, bz = float(default_b[0]), float(default_b[1]), float(default_b[2])

    a = np.array([ax, ay, az], dtype=float)
    b = np.array([bx, by, bz], dtype=float)
    fig, explain = make_formula_step_figure(a, b, step, lang)
    steps = get_steps(TOPIC_ID, lang)
    label = steps[step]["title"]
    return (
        fig,
        explain,
        step,
        label,
        ax,
        ay,
        az,
        bx,
        by,
        bz,
        *i18n,
    )


dash.register_page(
    __name__,
    path="/skalyarnoe",
    name="Dot product",
    order=2,
    layout=layout,
)
