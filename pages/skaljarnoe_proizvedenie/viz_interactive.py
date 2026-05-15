"""Interactive dot product visualization."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from dash_ui import SCENE_UIREVISION, scene_3d
from i18n import get_steps, step_count, t
from i18n.catalog import PRESET_IDS

from .viz import coordinate_formula, decomposition, projection_onto

TOPIC = "skalyarnoe"
STEP_COUNT = step_count(TOPIC)

VECTOR_PRESETS: dict[str, tuple[np.ndarray, np.ndarray]] = {
    "acute": (
        np.array([3.0, 1.0, 0.5]),
        np.array([1.0, 2.0, 0.0]),
    ),
    "right": (
        np.array([2.0, 0.0, 1.0]),
        np.array([0.0, 3.0, 0.0]),
    ),
    "obtuse": (
        np.array([2.0, 1.0, 0.0]),
        np.array([-1.5, 2.0, 0.5]),
    ),
    "parallel": (
        np.array([1.5, 1.0, 0.5]),
        np.array([3.0, 2.0, 1.0]),
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
            hovertemplate=f"<b>{name}</b><br>x=%{{x:.2f}} y=%{{y:.2f}} z=%{{z:.2f}}<extra></extra>",
        )
    )


def _stats_text(a: np.ndarray, b: np.ndarray, step: int, lang: str) -> str:
    c, na, nb, proj, orth, phi = decomposition(a, b)
    total, terms = coordinate_formula(a, b)
    deg = np.degrees(phi)
    lines = [
        f"a = [{a[0]:.3f}, {a[1]:.3f}, {a[2]:.3f}]   |a| = {na:.4f}",
        f"b = [{b[0]:.3f}, {b[1]:.3f}, {b[2]:.3f}]   |b| = {nb:.4f}",
        "",
        f"a · b = {c:.4f}",
        f"|a||b|cos φ = {na * nb * np.cos(phi):.4f}   (φ = {deg:.2f}°)",
        "",
        t("skalyarnoe.stats.coords", lang),
    ]
    labels = ["₁", "₂", "₃"]
    for i, (ai, bi, ti) in enumerate(terms):
        lab = labels[i] if i < 3 else str(i + 1)
        lines.append(f"  a{lab}b{lab} = {ai:.3f}·{bi:.3f} = {ti:.4f}")
    lines.append(f"  sum = {total:.4f}")
    if step >= 3:
        lines.append(
            "\n"
            + t(
                "skalyarnoe.stats.orthogonal",
                lang,
                ok=abs(c) < 1e-9,
                val=f"{c:.2e}",
            )
        )
    if step >= 4:
        lines.extend(
            [
                "",
                f"proj_b(a) = [{proj[0]:.3f}, {proj[1]:.3f}, {proj[2]:.3f}]",
                f"residual ⊥ b:  (a−proj)·b = {np.dot(orth, b):.2e}",
            ]
        )
    if step >= 5:
        lhs = np.linalg.norm(a + b) ** 2
        rhs = na**2 + 2 * c + nb**2
        lines.append(
            "\n"
            + t(
                "skalyarnoe.stats.identity",
                lang,
                lhs=f"{lhs:.4f}",
                rhs=f"{rhs:.4f}",
                ok=np.isclose(lhs, rhs),
            )
        )
    return "\n".join(lines)


def make_formula_step_figure(
    a: np.ndarray,
    b: np.ndarray,
    step: int,
    lang: str = "en",
) -> tuple[go.Figure, str]:
    steps = get_steps(TOPIC, lang)
    step = max(0, min(step, len(steps) - 1))
    meta = steps[step]
    origin = np.zeros(3)
    c, na, nb, proj, orth, phi = decomposition(a, b)

    fig = go.Figure()
    _add_segment(fig, origin, a, color="#534AB7", name="a", width=7)
    _add_segment(fig, origin, b, color="#0F6E56", name="b", width=7)

    if step == 1:
        for i, (ai, bi, ti) in enumerate(coordinate_formula(a, b)[1]):
            comp_a = np.zeros(3)
            comp_b = np.zeros(3)
            comp_a[i] = ai
            comp_b[i] = bi
            _add_segment(
                fig, origin, comp_a, color="#888888", name=f"a{i+1}e{i+1}", width=2, dash="dot"
            )
            _add_segment(
                fig, comp_a, comp_a + comp_b,
                color="#2E8BC0", name=f"+a{i+1}b{i+1}", width=3, dash="dash",
            )
    elif step == 2:
        nb_vec = b / (nb + 1e-12)
        scale = 0.35 * min(na, nb)
        arc_end = nb_vec * scale * np.cos(phi) + np.cross(nb_vec, a / (na + 1e-12)) * scale * np.sin(phi)
        if np.linalg.norm(arc_end) > 1e-6:
            _add_segment(fig, origin, arc_end, color="#BA7517", name=f"φ ≈ {np.degrees(phi):.1f}°", width=4)
    elif step == 3:
        if abs(c) < 1e-6:
            _add_segment(fig, origin, a, color="#534AB7", name="a ⊥ b", width=5)
            _add_segment(fig, origin, b, color="#0F6E56", name="", width=5)
        else:
            _add_segment(
                fig, origin, proj, color="#BA7517", name="not ⊥: projection shown", width=4, dash="dash"
            )
    elif step == 4:
        _add_segment(fig, origin, proj, color="#BA7517", name="proj_b(a)", width=7)
        _add_segment(fig, proj, a, color="#D85A30", name="a − proj", width=5, dash="dash")
        _add_segment(fig, origin, b, color="#0F6E56", name="b", width=4)
    elif step == 5:
        _add_segment(fig, origin, proj, color="#BA7517", name="proj_b(a)", width=5)
        _add_segment(fig, origin, a + b, color="#9B59B6", name="a + b", width=6)
    elif step == 6:
        _add_segment(fig, origin, proj, color="#BA7517", name="proj (projection)", width=5)
        _add_segment(fig, proj, a, color="#D85A30", name="orthogonal part", width=4, dash="dash")

    fig.update_layout(
        uirevision=SCENE_UIREVISION,
        title=dict(text=meta["title"], x=0.5, font=dict(size=16)),
        scene=scene_3d(),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"),
        margin=dict(l=0, r=0, t=55, b=0),
        height=720,
    )
    explain = f"{meta['explain']}\n\n{meta['formula']}\n\n{_stats_text(a, b, step, lang)}"
    return fig, explain
