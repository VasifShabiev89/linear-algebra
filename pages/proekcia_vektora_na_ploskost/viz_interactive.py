"""Interactive 3D visualization (Plotly): rotate, zoom, tooltips, sliders."""

from __future__ import annotations

import webbrowser
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash_ui import SCENE_UIREVISION, scene_3d
from i18n import get_steps, step_count, t
from i18n.catalog import PRESET_IDS

from .viz import OUT_DIR, _param_ranges, formula_decomposition, orthonormal_basis, project_onto_plane

TOPIC = "proekcia"
STEP_COUNT = step_count(TOPIC)

PLANE_PRESETS: dict[str, tuple[np.ndarray, np.ndarray]] = {
    "xy": (
        np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]),
        np.array([2.0, 3.0, 7.0]),
    ),
    "tilted": (
        np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
        np.array([1.0, 1.0, 0.0]),
    ),
    "general": (
        np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
        np.array([1.5, 0.5, 2.5]),
    ),
}

PRESET_ORDER: tuple[str, ...] = PRESET_IDS[TOPIC]


def _add_segment(
    fig: go.Figure,
    start: np.ndarray,
    end: np.ndarray,
    *,
    color: str,
    name: str,
    width: int = 6,
    dash: str | None = None,
    row: int | None = None,
    col: int | None = None,
) -> None:
    trace = go.Scatter3d(
      x=[start[0], end[0]],
      y=[start[1], end[1]],
      z=[start[2], end[2]],
      mode="lines+markers",
      name=name,
      line=dict(color=color, width=width, dash=dash),
      marker=dict(size=[2, 7], color=color),
        hovertemplate=(
            f"<b>{name}</b><br>"
            "x=%{x:.2f} y=%{y:.2f} z=%{z:.2f}<extra></extra>"
        ),
    )
    if row is not None and col is not None:
        fig.add_trace(trace, row=row, col=col)
    else:
        fig.add_trace(trace)


def _add_plane(
    fig: go.Figure,
    A: np.ndarray,
    v: np.ndarray,
    *,
    u1: np.ndarray | None = None,
    u2: np.ndarray | None = None,
) -> None:
    s_range, t_range = _param_ranges(A, v)
    s = np.linspace(s_range[0], s_range[1], 18)
    t = np.linspace(t_range[0], t_range[1], 18)
    S, T = np.meshgrid(s, t)
    if u1 is not None and u2 is not None:
        px = S * u1[0] + T * u2[0]
        py = S * u1[1] + T * u2[1]
        pz = S * u1[2] + T * u2[2]
    else:
        px = S * A[0, 0] + T * A[0, 1]
        py = S * A[1, 0] + T * A[1, 1]
        pz = S * A[2, 0] + T * A[2, 1]
    fig.add_trace(
        go.Surface(
            x=px, y=py, z=pz,
            colorscale=[[0, "rgba(15,110,86,0.12)"], [1, "rgba(93,202,165,0.32)"]],
            showscale=False,
            hoverinfo="skip",
            name="plane W",
        )
    )


def _formula_stats(
    v: np.ndarray,
    u1: np.ndarray,
    u2: np.ndarray,
    c1: float,
    c2: float,
    comp1: np.ndarray,
    comp2: np.ndarray,
    proj: np.ndarray,
    residual: np.ndarray,
    step: int,
    lang: str,
) -> str:
    lines = [
        t("proekcia.stats.header", lang),
        "",
        f"v·u₁ = {c1:.4f}      |comp₁| = {np.linalg.norm(comp1):.4f}",
        f"v·u₂ = {c2:.4f}      |comp₂| = {np.linalg.norm(comp2):.4f}",
        "",
        f"proj  = [{proj[0]:.3f}, {proj[1]:.3f}, {proj[2]:.3f}]",
        f"residual·u₁ = {np.dot(residual, u1):.2e}   residual·u₂ = {np.dot(residual, u2):.2e}",
    ]
    if step >= 5:
        check = np.allclose(proj, comp1 + comp2)
        lines.append("\n" + t("proekcia.stats.check", lang, ok=check))
    return "\n".join(lines)


def make_formula_step_figure(
    A: np.ndarray,
    v: np.ndarray,
    step: int,
    lang: str = "en",
) -> tuple[go.Figure, str]:
    """Step-by-step formula visualization; step is index 0..6."""
    steps = get_steps(TOPIC, lang)
    step = max(0, min(step, len(steps) - 1))
    meta = steps[step]

    u1, u2 = orthonormal_basis(A)
    c1, c2, comp1, comp2, proj, residual = formula_decomposition(v, u1, u2)
    origin = np.zeros(3)

    fig = go.Figure()
    _add_plane(fig, A, v, u1=u1, u2=u2)

    if step <= 4:
        _add_segment(fig, origin, u1 * 1.4, color="#0F6E56", name="u₁", width=4)
        if step != 2:
            _add_segment(fig, origin, u2 * 1.4, color="#1D9E75", name="u₂", width=4)
    elif step == 5:
        _add_segment(fig, origin, u1, color="#0F6E56", name="u₁", width=3)
        _add_segment(fig, origin, u2, color="#1D9E75", name="u₂", width=3)

    _add_segment(fig, origin, v, color="#534AB7", name="v", width=7)

    foot1 = comp1
    foot2 = comp2

    if step == 1:
        _add_segment(fig, foot1, v, color="#888888", name="⊥ to u₁", width=3, dash="dot")
        _add_segment(fig, origin, foot1, color="#2E8BC0", name="(v·u₁)u₁ — shadow only", width=4, dash="dash")
    elif step == 2:
        _add_segment(fig, origin, comp1, color="#2E8BC0", name=f"(v·u₁)u₁,  v·u₁={c1:.2f}", width=7)
    elif step == 3:
        _add_segment(fig, origin, comp1, color="#2E8BC0", name=f"(v·u₁)u₁ = {c1:.2f}", width=4)
        _add_segment(fig, foot2, v, color="#888888", name="⊥ to u₂", width=3, dash="dot")
        _add_segment(fig, origin, foot2, color="#9B59B6", name="(v·u₂)u₂ — shadow", width=4, dash="dash")
    elif step == 4:
        _add_segment(fig, origin, comp1, color="#2E8BC0", name="(v·u₁)u₁", width=4)
        _add_segment(fig, origin, comp2, color="#9B59B6", name=f"(v·u₂)u₂,  v·u₂={c2:.2f}", width=7)
    elif step == 5:
        _add_segment(fig, origin, comp1, color="#2E8BC0", name="(v·u₁)u₁", width=6)
        _add_segment(fig, comp1, comp1 + comp2, color="#9B59B6", name="(v·u₂)u₂", width=6)
        _add_segment(fig, origin, proj, color="#BA7517", name="proj_W(v) = sum", width=7)
        _add_segment(fig, comp1, proj, color="#9B59B6", width=2, dash="dot", name="")
    elif step == 6:
        _add_segment(fig, origin, proj, color="#BA7517", name="proj_W(v)", width=7)
        _add_segment(fig, proj, v, color="#D85A30", name="v − proj", width=5, dash="dash")
    elif step == 0:
        _add_segment(fig, origin, u1, color="#0F6E56", name="u₁ (|u₁|=1)", width=5)
        _add_segment(fig, origin, u2, color="#1D9E75", name="u₂ (|u₂|=1)", width=5)

    fig.update_layout(
        uirevision=SCENE_UIREVISION,
        title=dict(text=meta["title"], x=0.5, font=dict(size=16)),
        scene=scene_3d(),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"),
        margin=dict(l=0, r=0, t=55, b=0),
        height=720,
    )
    explain = (
        f"{meta['explain']}\n\n{meta['formula']}\n\n"
        f"{_formula_stats(v, u1, u2, c1, c2, comp1, comp2, proj, residual, step, lang)}"
    )
    return fig, explain


def make_projection_figure(
    A: np.ndarray,
    v: np.ndarray,
    *,
    title: str | None = None,
) -> tuple[go.Figure, np.ndarray, np.ndarray]:
    proj, residual = project_onto_plane(A, v)
    s_range, t_range = _param_ranges(A, v)

    s = np.linspace(s_range[0], s_range[1], 20)
    t = np.linspace(t_range[0], t_range[1], 20)
    S, T = np.meshgrid(s, t)
    plane_x = S * A[0, 0] + T * A[0, 1]
    plane_y = S * A[1, 0] + T * A[1, 1]
    plane_z = S * A[2, 0] + T * A[2, 1]

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=plane_x,
            y=plane_y,
            z=plane_z,
            colorscale=[[0, "rgba(15,110,86,0.15)"], [1, "rgba(93,202,165,0.35)"]],
            showscale=False,
            hoverinfo="skip",
            name="plane W",
        )
    )

    origin = np.zeros(3)
    _add_segment(fig, origin, A[:, 0], color="#0F6E56", name="a₁", width=5)
    _add_segment(fig, origin, A[:, 1], color="#1D9E75", name="a₂", width=5)
    _add_segment(fig, origin, v, color="#534AB7", name="v", width=7)
    _add_segment(fig, origin, proj, color="#BA7517", name="proj", width=7)
    _add_segment(
        fig, proj, v, color="#D85A30", name="residual (v − proj)", width=5, dash="dash"
    )

    fig.update_layout(
        uirevision=SCENE_UIREVISION,
        title=dict(
            text=title or "Projection of v onto plane W = span(a₁, a₂)",
            x=0.5,
        ),
        scene=scene_3d(initial_eye=(1.6, 1.4, 1.1)),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
        margin=dict(l=0, r=0, t=50, b=0),
        height=700,
    )
    return fig, proj, residual


def _stats_text(A: np.ndarray, v: np.ndarray, proj: np.ndarray, residual: np.ndarray) -> str:
    return (
        f"v       = [{v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f}]\n"
        f"proj    = [{proj[0]:.2f}, {proj[1]:.2f}, {proj[2]:.2f}]   |proj| = {np.linalg.norm(proj):.3f}\n"
        f"residual = [{residual[0]:.2f}, {residual[1]:.2f}, {residual[2]:.2f}]   |residual| = {np.linalg.norm(residual):.3f}\n"
        f"residual·a₁ = {A[:, 0] @ residual:.2e}   residual·a₂ = {A[:, 1] @ residual:.2e}  (≈ 0)\n"
        f"|v|² = {np.linalg.norm(v) ** 2:.3f}  =  |proj|² + |residual|²  "
        f"({np.linalg.norm(proj) ** 2:.3f} + {np.linalg.norm(residual) ** 2:.3f})"
    )


def show_interactive(
    A: np.ndarray,
    v: np.ndarray,
    *,
    title: str | None = None,
    html_name: str = "projection.html",
) -> None:
    fig, proj, residual = make_projection_figure(A, v, title=title)
    print(_stats_text(A, v, proj, residual))

    html_path = OUT_DIR / html_name
    fig.write_html(html_path, include_plotlyjs="cdn", auto_open=False)
    print(f"\nInteractive plot: {html_path}")
    print("  • drag to rotate, scroll to zoom, Shift+drag to pan")
    print("  • hover over arrows for coordinates")
    webbrowser.open(html_path.as_uri())
    fig.show()


def make_cases_figure(
    A: np.ndarray,
    cases: dict[str, np.ndarray],
    *,
    suptitle: str,
) -> go.Figure:
    n = len(cases)
    cols = 2
    rows = (n + 1) // 2
    titles = list(cases.keys())
    fig = make_subplots(
        rows=rows,
        cols=cols,
        specs=[[{"type": "scene"}] * cols for _ in range(rows)],
        subplot_titles=titles,
        horizontal_spacing=0.05,
        vertical_spacing=0.08,
    )

    for idx, (name, v) in enumerate(cases.items()):
        row = idx // cols + 1
        col = idx % cols + 1
        proj, residual = project_onto_plane(A, v)
        s_range, t_range = _param_ranges(A, v, margin=0.3)
        s = np.linspace(s_range[0], s_range[1], 12)
        t = np.linspace(t_range[0], t_range[1], 12)
        S, T = np.meshgrid(s, t)
        px = S * A[0, 0] + T * A[0, 1]
        py = S * A[1, 0] + T * A[1, 1]
        pz = S * A[2, 0] + T * A[2, 1]

        fig.add_trace(
            go.Surface(
                x=px, y=py, z=pz,
                colorscale=[[0, "rgba(15,110,86,0.12)"], [1, "rgba(93,202,165,0.3)"]],
                showscale=False,
                hoverinfo="skip",
                name=f"{name}: plane",
                legendgroup=name,
                showlegend=False,
            ),
            row=row,
            col=col,
        )
        origin = np.zeros(3)
        _add_segment(fig, origin, v, color="#534AB7", name=f"{name}: v", row=row, col=col)
        _add_segment(fig, origin, proj, color="#BA7517", name=f"{name}: proj", row=row, col=col)
        _add_segment(
            fig, proj, v, color="#D85A30", name=f"{name}: residual",
            dash="dash", row=row, col=col,
        )

    fig.update_scenes(aspectmode="data")
    fig.update_layout(
        title=dict(text=suptitle, x=0.5),
        height=800,
        margin=dict(t=80),
    )
    return fig


def make_regression_figure(
    x_data: np.ndarray,
    y_data: np.ndarray,
    y_hat: np.ndarray,
    y_true: np.ndarray,
    residuals: np.ndarray,
) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "OLS: y is projection onto columns of X",
            "Residuals ⊥ columns of X",
        ),
        horizontal_spacing=0.1,
    )

    fig.add_trace(
        go.Scatter(x=x_data, y=y_data, mode="markers", name="data (y)",
                   marker=dict(color="#534AB7", size=9)),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=x_data, y=y_hat, mode="lines", name="fit Xw = proj",
                   line=dict(color="#BA7517", width=3)),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=x_data, y=y_true, mode="lines", name="true curve",
                   line=dict(color="#0F6E56", width=2, dash="dash")),
        row=1, col=1,
    )
    for xi, yi, yhi in zip(x_data, y_data, y_hat):
        fig.add_trace(
            go.Scatter(
                x=[xi, xi], y=[yi, yhi], mode="lines",
                line=dict(color="#D85A30", width=1),
                showlegend=False,
                hoverinfo="skip",
            ),
            row=1, col=1,
        )

    fig.add_trace(
        go.Scatter(x=x_data, y=residuals, mode="markers", name="residuals",
                   marker=dict(color="#D85A30", size=9)),
        row=1, col=2,
    )
    fig.add_hline(y=0, line_width=1, line_color="black", row=1, col=2)

    fig.update_xaxes(title_text="x", row=1, col=1)
    fig.update_yaxes(title_text="y", row=1, col=1)
    fig.update_xaxes(title_text="x", row=1, col=2)
    fig.update_yaxes(title_text="y − ŷ", row=1, col=2)
    fig.update_layout(
        title="Step 5: linear regression as projection",
        height=500,
        legend=dict(x=0.02, y=0.98),
    )
    return fig


def open_figure(fig: go.Figure, html_path: Path) -> None:
    fig.write_html(html_path, include_plotlyjs="cdn", auto_open=False)
    print(f"Interactive plot: {html_path}")
    webbrowser.open(html_path.as_uri())
    fig.show()
