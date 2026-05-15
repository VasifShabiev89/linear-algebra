"""Dot product: computation and decomposition."""

from __future__ import annotations

import numpy as np


def dot(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def norms(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    return float(np.linalg.norm(a)), float(np.linalg.norm(b))


def angle_rad(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = norms(a, b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    cos_phi = np.clip(dot(a, b) / (na * nb), -1.0, 1.0)
    return float(np.arccos(cos_phi))


def are_orthogonal(a: np.ndarray, b: np.ndarray, tol: float = 1e-9) -> bool:
    return abs(dot(a, b)) < tol


def projection_onto(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Projection of a onto direction b: proj_b(a) = ((a·b)/|b|²) b."""
    nb2 = float(np.dot(b, b))
    if nb2 < 1e-12:
        return np.zeros_like(a)
    return (dot(a, b) / nb2) * b


def rejection_from(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Component of a orthogonal to b: a − proj_b(a)."""
    return a - projection_onto(a, b)


def decomposition(
    a: np.ndarray, b: np.ndarray
) -> tuple[float, float, float, np.ndarray, np.ndarray, float]:
    """
    a·b, |a|, |b|, proj_b(a), orth_a_to_b, angle in radians.
    """
    c = dot(a, b)
    na, nb = norms(a, b)
    proj = projection_onto(a, b)
    orth = a - proj
    phi = angle_rad(a, b)
    return c, na, nb, proj, orth, phi


def coordinate_formula(a: np.ndarray, b: np.ndarray) -> tuple[float, list[tuple[float, float, float]]]:
    """Sum of coordinate products and list of (aᵢ, bᵢ, aᵢbᵢ)."""
    terms: list[tuple[float, float, float]] = []
    total = 0.0
    for i in range(len(a)):
        t = float(a[i] * b[i])
        terms.append((float(a[i]), float(b[i]), t))
        total += t
    return total, terms
