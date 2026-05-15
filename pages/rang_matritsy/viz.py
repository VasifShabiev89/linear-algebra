"""Matrix rank: column independence and dimensions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class RankInfo:
    rank: int
    n_cols: int
    n_rows: int
    independent_cols: tuple[int, ...]
    dependent_cols: tuple[int, ...]
    nullity: int


def column_vectors(A: np.ndarray) -> list[np.ndarray]:
    return [A[:, j].astype(float) for j in range(A.shape[1])]


def _in_span(v: np.ndarray, basis: list[np.ndarray], tol: float = 1e-8) -> bool:
    if not basis:
        return np.linalg.norm(v) < tol
    B = np.column_stack(basis)
    if B.shape[0] != len(v):
        return False
    coeffs, residuals, _, _ = np.linalg.lstsq(B, v, rcond=None)
    approx = B @ coeffs
    return float(np.linalg.norm(v - approx)) < tol


def independent_column_indices(A: np.ndarray, tol: float = 1e-8) -> list[int]:
    """Greedy selection of linearly independent (pivot) columns."""
    cols = column_vectors(A)
    basis: list[np.ndarray] = []
    independent: list[int] = []
    for j, col in enumerate(cols):
        if np.linalg.norm(col) < tol:
            continue
        if not _in_span(col, basis, tol):
            basis.append(col)
            independent.append(j)
    return independent


def analyze_rank(A: np.ndarray) -> RankInfo:
    A = np.asarray(A, dtype=float)
    n_rows, n_cols = A.shape
    indep = tuple(independent_column_indices(A))
    dep = tuple(j for j in range(n_cols) if j not in indep)
    r = int(np.linalg.matrix_rank(A))
    if len(indep) != r and n_cols > 0:
        r = len(indep)
    nullity = n_cols - r if n_cols >= r else 0
    return RankInfo(
        rank=r,
        n_cols=n_cols,
        n_rows=n_rows,
        independent_cols=indep,
        dependent_cols=dep,
        nullity=nullity,
    )


def row_rank(A: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(A.T))
