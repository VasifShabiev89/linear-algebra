"""Interactive matrix rank visualization via columns."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from dash_ui import SCENE_UIREVISION, scene_3d
from i18n import get_steps, preset_hint, step_count, t
from i18n.catalog import PRESET_IDS

from .viz import RankInfo, analyze_rank, column_vectors

TOPIC = "rang"
STEP_COUNT = step_count(TOPIC)

MATRIX_PRESETS: dict[str, np.ndarray] = {
    "r22": np.array([[2.0, 0.5], [0.5, 1.5]]),
    "r21": np.array([[1.0, 2.0], [2.0, 4.0]]),
    "r32": np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]),
    "r33": np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]]),
}

PRESET_ORDER: tuple[str, ...] = PRESET_IDS[TOPIC]


def _pad_to_3d(v: np.ndarray) -> np.ndarray:
    out = np.zeros(3)
    out[: min(3, len(v))] = v[: min(3, len(v))]
    return out


def _add_column(
    fig: go.Figure,
    col: np.ndarray,
    *,
    color: str,
    name: str,
    width: int = 6,
    dash: str | None = None,
) -> None:
    origin = np.zeros(3)
    end = _pad_to_3d(col)
    _add_segment(fig, origin, end, color=color, name=name, width=width, dash=dash)


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
            marker=dict(size=[2, 8], color=color),
            hovertemplate=f"<b>{name}</b><br>x=%{{x:.2f}} y=%{{y:.2f}} z=%{{z:.2f}}<extra></extra>",
        )
    )


def _add_span_plane(fig: go.Figure, c1: np.ndarray, c2: np.ndarray, info: RankInfo) -> None:
    if info.rank < 2:
        return
    u1 = _pad_to_3d(c1)
    u2 = _pad_to_3d(c2)
    if np.linalg.norm(u2) < 1e-9:
        return
    s = np.linspace(-1.5, 1.5, 14)
    t = np.linspace(-1.5, 1.5, 14)
    S, T = np.meshgrid(s, t)
    px = S * u1[0] + T * u2[0]
    py = S * u1[1] + T * u2[1]
    pz = S * u1[2] + T * u2[2]
    fig.add_trace(
        go.Surface(
            x=px, y=py, z=pz,
            colorscale=[[0, "rgba(15,110,86,0.1)"], [1, "rgba(93,202,165,0.28)"]],
            showscale=False,
            hoverinfo="skip",
            name="Col(A)",
        )
    )


def _add_span_line(fig: go.Figure, c: np.ndarray) -> None:
    u = _pad_to_3d(c)
    if np.linalg.norm(u) < 1e-9:
        return
    t = np.linspace(-2.0, 2.0, 30)
    pts = np.outer(t, u)
    fig.add_trace(
        go.Scatter3d(
            x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
            mode="lines",
            line=dict(color="rgba(186,117,23,0.5)", width=4),
            name="line span(c₁)",
            hoverinfo="skip",
        )
    )


def _matrix_text(A: np.ndarray, info: RankInfo, step: int, lang: str) -> str:
    cols = column_vectors(A)
    lines = [
        t("rang.stats.size", lang, rows=info.n_rows, cols=info.n_cols),
        t("rang.stats.rank", lang, rank=info.rank),
        t(
            "rang.stats.nullity",
            lang,
            nullity=info.nullity,
            n=info.n_cols,
            rank=info.rank,
        ),
        "",
        t("rang.stats.columns", lang),
    ]
    for j, c in enumerate(cols):
        tag_key = "rang.stats.col_pivot" if j in info.independent_cols else "rang.stats.col_dependent"
        tag = t(tag_key, lang)
        z = f", {c[2]:.3f}" if len(c) > 2 else ""
        lines.append(f"  c{j+1} = [{c[0]:.3f}, {c[1]:.3f}{z}]  ({tag})")
    if step >= 5:
        rr = int(np.linalg.matrix_rank(A.T))
        lines.append(
            "\n"
            + t(
                "rang.stats.rank_transpose",
                lang,
                rr=rr,
                match=rr == info.rank,
            )
        )
    if step >= 6:
        lines.append(
            "\n"
            + t(
                "rang.stats.theorem",
                lang,
                rank=info.rank,
                nullity=info.nullity,
                n=info.n_cols,
            )
        )
    if step >= 7:
        lines.append("\n" + t("rang.stats.systems", lang))
    return "\n".join(lines)


def make_formula_step_figure(
    A: np.ndarray,
    step: int,
    lang: str = "en",
) -> tuple[go.Figure, str]:
    steps = get_steps(TOPIC, lang)
    step = max(0, min(step, len(steps) - 1))
    meta = steps[step]
    info = analyze_rank(A)
    cols = column_vectors(A)
    colors_indep = ["#0F6E56", "#1D9E75", "#2E8BC0", "#534AB7"]
    colors_dep = "#a1a1aa"

    fig = go.Figure()

    if step >= 2 and info.rank == 2 and len(info.independent_cols) >= 2:
        i0, i1 = info.independent_cols[0], info.independent_cols[1]
        _add_span_plane(fig, cols[i0], cols[i1], info)
    elif step >= 2 and info.rank == 1 and cols:
        _add_span_line(fig, cols[info.independent_cols[0]] if info.independent_cols else cols[0])

    for j, col in enumerate(cols):
        indep = j in info.independent_cols
        if step < 3:
            color = colors_indep[j % len(colors_indep)]
            dash = None
            width = 6
        elif indep:
            color = colors_indep[j % len(colors_indep)]
            dash = None
            width = 7
        else:
            color = colors_dep
            dash = "dash"
            width = 5
        label = f"c{j+1}" + (" ✓" if indep else " (dep.)")
        if step == 1:
            label = f"c{j+1} — column {j+1}"
        _add_column(fig, col, color=color, name=label, width=width, dash=dash)

    if step >= 4 and info.dependent_cols:
        j = info.dependent_cols[0]
        if info.independent_cols:
            i0 = info.independent_cols[0]
            dep = cols[j]
            base = cols[i0]
            if np.linalg.norm(base) > 1e-9:
                coeff = float(np.dot(dep, base) / np.dot(base, base))
                combo = coeff * _pad_to_3d(base)
                _add_segment(
                    fig, combo, _pad_to_3d(dep),
                    color="#D85A30", name="dependence", width=3, dash="dot",
                )

    fig.update_layout(
        uirevision=SCENE_UIREVISION,
        title=dict(text=meta["title"], x=0.5, font=dict(size=16)),
        scene=scene_3d(),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"),
        margin=dict(l=0, r=0, t=55, b=0),
        height=720,
    )
    explain = f"{meta['explain']}\n\n{meta['formula']}\n\n{_matrix_text(A, info, step, lang)}"
    return fig, explain
