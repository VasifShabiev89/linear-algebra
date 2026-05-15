"""Topic catalog: add an entry here and create a page under pages/."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Topic:
    id: str
    path: str
    formula: str | None = None
    tag_key: str | None = None


TOPICS: tuple[Topic, ...] = (
    Topic(
        id="proekcia",
        path="/proekcia",
        formula="proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂",
        tag_key="3D",
    ),
    Topic(
        id="skalyarnoe",
        path="/skalyarnoe",
        formula="a · b = |a||b|cos φ = a₁b₁ + a₂b₂ + …",
        tag_key="3D",
    ),
    Topic(
        id="rang",
        path="/rang",
        formula="rank(A) + nullity(A) = n",
        tag_key="3D",
    ),
)
