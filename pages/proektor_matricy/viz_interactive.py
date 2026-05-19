"""Interactive 3D: non-orthogonal projector formula as measure → correct → assemble."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from dash_ui import SCENE_UIREVISION, scene_3d
from i18n import get_steps, step_count, t
from i18n.catalog import PRESET_IDS

from .viz import (
    column_decomposition,
    coefficients,
    dirty_probe,
    naive_from_probe,
    param_ranges,
    project,
)

TOPIC = "proektor"
STEP_COUNT = step_count(TOPIC)

MATRIX_PRESETS: dict[str, tuple[np.ndarray, np.ndarray]] = {
    "tilted": (
        np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
        np.array([1.0, 1.0, 0.0]),
    ),
    "oblique": (
        np.array([[1.2, 0.4], [0.3, 1.0], [0.8, 0.6]]),
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
) -> None:
    fig.add_trace(
        go.Scatter3d(
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
    )


def _add_point(
    fig: go.Figure,
    point: np.ndarray,
    *,
    color: str,
    name: str,
    size: int = 6,
) -> None:
    fig.add_trace(
        go.Scatter3d(
            x=[point[0]],
            y=[point[1]],
            z=[point[2]],
            mode="markers+text",
            name=name,
            marker=dict(size=size, color=color),
            text=[name],
            textposition="top center",
            hovertemplate=(
                f"<b>{name}</b><br>"
                "x=%{x:.2f} y=%{y:.2f} z=%{z:.2f}<extra></extra>"
            ),
        )
    )


def _add_plane(fig: go.Figure, A: np.ndarray, v: np.ndarray) -> None:
    s_range, t_range = param_ranges(A, v)
    s = np.linspace(s_range[0], s_range[1], 18)
    t = np.linspace(t_range[0], t_range[1], 18)
    S, T = np.meshgrid(s, t)
    px = S * A[0, 0] + T * A[0, 1]
    py = S * A[1, 0] + T * A[1, 1]
    pz = S * A[2, 0] + T * A[2, 1]
    fig.add_trace(
        go.Surface(
            x=px,
            y=py,
            z=pz,
            colorscale=[[0, "rgba(15,110,86,0.12)"], [1, "rgba(93,202,165,0.32)"]],
            showscale=False,
            hoverinfo="skip",
            name="Col(A)",
        )
    )


def _angle_deg(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    c = float(np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0))
    return float(np.degrees(np.arccos(c)))


def _formula_stats(
    A: np.ndarray,
    v: np.ndarray,
    x: np.ndarray,
    proj: np.ndarray,
    residual: np.ndarray,
    step: int,
    lang: str,
) -> str:
    dirty = dirty_probe(A, v)
    wrong = naive_from_probe(A, v)
    ata = A.T @ A
    inv_ata = np.linalg.inv(ata)
    a1, a2 = A[:, 0], A[:, 1]
    angle = _angle_deg(a1, a2)
    dist_wrong = float(np.linalg.norm(wrong - proj))
    residual_norm = float(np.linalg.norm(residual))

    lines: list[str] = []

    if step <= 1:
        lines.append(t("proektor.stats.goal", lang))
    if step == 2:
        lines.append(
            t(
                "proektor.stats.mixing_angle",
                lang,
                angle=angle,
                hint=t("proektor.stats.mixing_hint", lang),
            )
        )
        lines.append(
            f"AᵀA off-diag a₁·a₂ = {ata[0, 1]:.4f}  "
            f"(diag: |a₁|²={ata[0, 0]:.3f}, |a₂|²={ata[1, 1]:.3f})"
        )
    if step in (3, 4):
        lines.extend(
            [
                t("proektor.stats.conveyor1", lang),
                t(
                    "proektor.stats.dirty",
                    lang,
                    d1=dirty[0],
                    d2=dirty[1],
                    a1v=dirty[0],
                    a2v=dirty[1],
                ),
            ]
        )
    if step == 4:
        lines.extend(
            [
                "",
                t("proektor.stats.wrong_guess", lang, dist=dist_wrong),
                t("proektor.stats.wrong_note", lang),
            ]
        )
    if step in (5, 6):
        lines.extend(
            [
                t("proektor.stats.conveyor2", lang),
                f"AᵀA = [[{ata[0,0]:.3f}, {ata[0,1]:.3f}],",
                f"       [{ata[1,0]:.3f}, {ata[1,1]:.3f}]]",
                t(
                    "proektor.stats.off_diag",
                    lang,
                    val=ata[0, 1],
                ),
            ]
        )
    if step == 6:
        lines.extend(
            [
                f"(AᵀA)⁻¹ = [[{inv_ata[0,0]:.3f}, {inv_ata[0,1]:.3f}],",
                f"          [{inv_ata[1,0]:.3f}, {inv_ata[1,1]:.3f}]]",
                t("proektor.stats.solve", lang),
            ]
        )
    if step >= 7:
        lines.extend(
            [
                "",
                t(
                    "proektor.stats.clean",
                    lang,
                    x1=x[0],
                    x2=x[1],
                    d1=dirty[0],
                    d2=dirty[1],
                ),
            ]
        )
    if step >= 8:
        comp1, comp2 = column_decomposition(A, x)
        lines.extend(
            [
                t("proektor.stats.conveyor3", lang),
                f"proj = [{proj[0]:.3f}, {proj[1]:.3f}, {proj[2]:.3f}]",
                t("proektor.stats.sum", lang, ok=np.allclose(comp1 + comp2, proj)),
            ]
        )
    if step >= 9:
        lines.extend(
            [
                "",
                f"|residual| = {residual_norm:.4f}",
                f"residual·a₁ ≈ {a1 @ residual:.2e}   residual·a₂ ≈ {a2 @ residual:.2e}",
                t("proektor.stats.same_projection", lang),
            ]
        )

    return "\n".join(lines) if lines else t("proektor.stats.header", lang)


def make_formula_step_figure(
    A: np.ndarray,
    v: np.ndarray,
    step: int,
    lang: str = "en",
) -> tuple[go.Figure, str]:
    steps = get_steps(TOPIC, lang)
    step = max(0, min(step, len(steps) - 1))
    meta = steps[step]

    a1, a2 = A[:, 0], A[:, 1]
    x = coefficients(A, v)
    dirty = dirty_probe(A, v)
    wrong = naive_from_probe(A, v)
    comp1, comp2 = column_decomposition(A, x)
    proj, residual, _, _ = project(A, v)
    origin = np.zeros(3)

    fig = go.Figure()
    _add_plane(fig, A, v)
    _add_segment(fig, origin, v, color="#534AB7", name="v", width=7)

    if step <= 1:
        _add_segment(fig, origin, a1 * 1.35, color="#0F6E56", name="a₁", width=6)
        _add_segment(fig, origin, a2 * 1.35, color="#1D9E75", name="a₂", width=6)
    elif step == 2:
        _add_segment(fig, origin, a1, color="#0F6E56", name="a₁", width=5)
        _add_segment(fig, origin, a2, color="#1D9E75", name="a₂ (not ⊥ a₁)", width=5)
        _add_segment(fig, a1, a1 + a2 * 0.35, color="#F59E0B", name="a₂ leaks into a₁ reading", width=4, dash="dash")
        _add_segment(fig, a2, a2 + a1 * 0.35, color="#F59E0B", name="a₁ leaks into a₂ reading", width=4, dash="dash")
    elif step == 3:
        _add_segment(fig, origin, a1, color="#0F6E56", name="a₁", width=4)
        _add_segment(fig, origin, a2, color="#1D9E75", name="a₂", width=4)
        _add_segment(
            fig,
            origin,
            float(dirty[0]) * a1,
            color="#2E8BC0",
            name=f"probe a₁·v = {dirty[0]:.2f}",
            width=5,
            dash="dash",
        )
        _add_segment(
            fig,
            origin,
            float(dirty[1]) * a2,
            color="#9B59B6",
            name=f"probe a₂·v = {dirty[1]:.2f}",
            width=5,
            dash="dash",
        )
        shadow1 = (float(dirty[0]) / float(a1 @ a1)) * a1
        shadow2 = (float(dirty[1]) / float(a2 @ a2)) * a2
        _add_point(fig, shadow1, color="#2E8BC0", name="shadow on a₁")
        _add_point(fig, shadow2, color="#9B59B6", name="shadow on a₂")
    elif step == 4:
        _add_segment(fig, origin, wrong, color="#E11D48", name="A(Aᵀv) — wrong!", width=7, dash="dot")
        _add_segment(fig, origin, proj, color="#BA7517", name="true proj", width=6)
        _add_segment(fig, wrong, proj, color="#888888", name="error", width=3, dash="dash")
    elif step in (5, 6):
        _add_segment(fig, origin, a1, color="#0F6E56", name="a₁", width=3, dash="dot")
        _add_segment(fig, origin, a2, color="#1D9E75", name="a₂", width=3, dash="dot")
        _add_segment(fig, origin, wrong, color="#E11D48", name="raw build", width=5, dash="dot")
        if step == 6:
            _add_segment(fig, origin, comp1, color="#2E8BC0", name=f"x₁a₁, x₁={x[0]:.2f}", width=6)
            _add_segment(fig, comp1, proj, color="#9B59B6", name="+ x₂a₂", width=5, dash="dash")
            _add_segment(fig, origin, proj, color="#BA7517", name="clean coeffs", width=7)
    elif step == 7:
        _add_segment(fig, origin, comp1, color="#2E8BC0", name=f"x₁a₁, x₁={x[0]:.2f}", width=6)
        _add_segment(fig, comp1, proj, color="#9B59B6", name=f"x₂a₂, x₂={x[1]:.2f}", width=6)
        _add_segment(fig, origin, proj, color="#BA7517", name="Ax with clean x", width=7)
    elif step == 8:
        _add_segment(fig, origin, comp1, color="#2E8BC0", name=f"x₁a₁", width=6)
        _add_segment(fig, comp1, proj, color="#9B59B6", name=f"x₂a₂", width=6)
        _add_segment(fig, origin, proj, color="#BA7517", name="A(AᵀA)⁻¹Aᵀv", width=8)
    elif step == 9:
        _add_segment(fig, origin, proj, color="#BA7517", name="proj", width=7)
        _add_segment(fig, proj, v, color="#D85A30", name="v − proj ⊥ plane", width=5, dash="dash")

    if step == 0:
        _add_segment(fig, origin, proj, color="#BA7517", name="closest on plane", width=6, dash="dash")
        _add_segment(fig, proj, v, color="#D85A30", name="residual", width=4, dash="dot")

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
        f"{_formula_stats(A, v, x, proj, residual, step, lang)}"
    )
    return fig, explain
