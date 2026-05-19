"""Matrix projector P = A(AᵀA)⁻¹Aᵀ and projection Pv onto Col(A)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

OUT_DIR = Path(__file__).resolve().parent


def coefficients(A: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Least-squares coefficients: AᵀAx = Aᵀv."""
    return np.linalg.solve(A.T @ A, A.T @ v)


def projection_matrix(A: np.ndarray) -> np.ndarray:
    """Orthogonal projector onto Col(A) when columns are independent."""
    return A @ np.linalg.inv(A.T @ A) @ A.T


def project(A: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Project v onto Col(A).

    Returns: proj, residual, x, P.
    """
    x = coefficients(A, v)
    proj = A @ x
    P = projection_matrix(A)
    return proj, v - proj, x, P


def dirty_probe(A: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Step 1 of the conveyor: Aᵀv — raw inner products with columns (often 'dirty')."""
    return A.T @ v


def naive_from_probe(A: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Wrong guess: treat Aᵀv as coefficients — works only when AᵀA = I."""
    return A @ dirty_probe(A, v)


def column_decomposition(
    A: np.ndarray,
    x: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """proj = x₁a₁ + x₂a₂ as components along matrix columns."""
    comp1 = float(x[0]) * A[:, 0]
    comp2 = float(x[1]) * A[:, 1]
    return comp1, comp2


def param_ranges(A: np.ndarray, v: np.ndarray, margin: float = 0.5) -> tuple[tuple[float, float], tuple[float, float]]:
    x = coefficients(A, v)
    smin = min(-margin, float(x[0]) - margin)
    smax = max(2.0, float(x[0]) + margin)
    tmin = min(-margin, float(x[1]) - margin)
    tmax = max(1.8, float(x[1]) + margin)
    return (smin, smax), (tmin, tmax)
