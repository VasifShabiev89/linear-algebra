"""Visualization of vector projection onto plane span(a1, a2)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent


def project_onto_plane(A: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    P = A @ np.linalg.inv(A.T @ A) @ A.T
    proj = P @ v
    return proj, v - proj


def orthonormal_basis(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Orthonormal basis u₁, u₂ of span(columns of A) — Gram–Schmidt."""
    a1 = A[:, 0].astype(float)
    a2 = A[:, 1].astype(float)
    u1 = a1 / np.linalg.norm(a1)
    a2_perp = a2 - np.dot(a2, u1) * u1
    u2 = a2_perp / np.linalg.norm(a2_perp)
    return u1, u2


def formula_decomposition(
    v: np.ndarray,
    u1: np.ndarray,
    u2: np.ndarray,
) -> tuple[float, float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂ for orthonormal u₁, u₂.

    Returns: c1, c2, comp1, comp2, proj, residual.
    """
    c1 = float(np.dot(v, u1))
    c2 = float(np.dot(v, u2))
    comp1 = c1 * u1
    comp2 = c2 * u2
    proj = comp1 + comp2
    residual = v - proj
    return c1, c2, comp1, comp2, proj, residual


def _param_ranges(A: np.ndarray, v: np.ndarray, margin: float = 0.5) -> tuple[tuple[float, float], tuple[float, float]]:
    x = np.linalg.solve(A.T @ A, A.T @ v)
    smin = min(-margin, float(x[0]) - margin)
    smax = max(2.0, float(x[0]) + margin)
    tmin = min(-margin, float(x[1]) - margin)
    tmax = max(1.8, float(x[1]) + margin)
    return (smin, smax), (tmin, tmax)


def plot_projection_3d(
    ax,
    A: np.ndarray,
    v: np.ndarray,
    *,
    title: str | None = None,
    s_range: tuple[float, float] | None = None,
    t_range: tuple[float, float] | None = None,
    elev: float = 18,
    azim: float = -55,
) -> tuple[np.ndarray, np.ndarray]:
    proj, residual = project_onto_plane(A, v)
    if s_range is None or t_range is None:
        s_range, t_range = _param_ranges(A, v)

    s = np.linspace(s_range[0], s_range[1], 15)
    t = np.linspace(t_range[0], t_range[1], 15)
    S, T = np.meshgrid(s, t)
    plane_x = S * A[0, 0] + T * A[0, 1]
    plane_y = S * A[1, 0] + T * A[1, 1]
    plane_z = S * A[2, 0] + T * A[2, 1]
    ax.plot_surface(
        plane_x, plane_y, plane_z,
        alpha=0.2, color="#0F6E56", edgecolor="#5DCAA5", linewidth=0.3,
    )

    origin = np.zeros(3)
    ax.quiver(*origin, *A[:, 0], color="#0F6E56", arrow_length_ratio=0.12, linewidth=2.5)
    ax.quiver(*origin, *A[:, 1], color="#1D9E75", arrow_length_ratio=0.12, linewidth=2.5)
    ax.text(*(A[:, 0] * 1.15), "a1", fontsize=11, color="#04342C", weight="bold")
    ax.text(*(A[:, 1] * 1.15), "a2", fontsize=11, color="#04342C", weight="bold")

    ax.quiver(*origin, *v, color="#534AB7", arrow_length_ratio=0.08, linewidth=3, label="v")
    ax.quiver(*origin, *proj, color="#BA7517", arrow_length_ratio=0.1, linewidth=3, label="proj")
    ax.plot(
        [proj[0], v[0]], [proj[1], v[1]], [proj[2], v[2]],
        color="#D85A30", linewidth=2, linestyle="--", label="residual",
    )
    ax.scatter(*v, color="#534AB7", s=60, zorder=10)
    ax.scatter(*proj, color="#BA7517", s=60, zorder=10)
    ax.scatter(0, 0, 0, color="black", s=40, zorder=10)

    ax.set_xlabel("X", fontsize=9)
    ax.set_ylabel("Y", fontsize=9)
    ax.set_zlabel("Z", fontsize=9)
    if title:
        ax.set_title(title, fontsize=10)
    ax.legend(loc="upper left", fontsize=8)
    ax.view_init(elev=elev, azim=azim)
    return proj, residual


def finish_figure(fig, png_path: Path | None = None) -> None:
    if png_path is not None:
        fig.savefig(png_path, dpi=110, bbox_inches="tight")
        print(f"Saved: {png_path}")

    if os.environ.get("PROEKCIA_NO_SHOW"):
        plt.close(fig)
        if png_path is not None:
            _open_in_viewer(png_path)
        return

    backend = plt.get_backend().lower()
    if backend == "agg":
        plt.close(fig)
        if png_path is not None:
            print("Interactive backend unavailable — opening PNG in viewer.")
            _open_in_viewer(png_path)
        return

    print("Close the plot window to continue.")
    plt.show()


def _open_in_viewer(path: Path) -> None:
    path = Path(path)
    if not path.exists():
        return
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", str(path)], check=False)


def show_projection(
    A: np.ndarray,
    v: np.ndarray,
    *,
    title: str,
    png_name: str,
    figsize: tuple[float, float] = (10, 8),
) -> None:
    if os.environ.get("PROEKCIA_STATIC"):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection="3d")
        proj, residual = plot_projection_3d(ax, A, v, title=title)
        print(f"  v        = {v}")
        print(f"  proj     = {np.round(proj, 4)}")
        print(f"  residual = {np.round(residual, 4)}")
        plt.tight_layout()
        finish_figure(fig, OUT_DIR / png_name)
        return

    from viz_interactive import show_interactive

    show_interactive(A, v, title=title, html_name=png_name.replace(".png", ".html"))
