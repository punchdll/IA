
from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

__all__ = ["Pos", "Grid", "manhattan", "euclidean", "chebyshev", "HEURISTICS"]

Pos = tuple[int, int]
HeuristicFn = Callable[[Pos, Pos], float]

_MOVES_4 = ((-1, 0), (1, 0), (0, -1), (0, 1))


def manhattan(a: Pos, b: Pos) -> float:
    """Distancia Manhattan entre dos posiciones (fila, col)."""
    return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))


def euclidean(a: Pos, b: Pos) -> float:
    """Distancia euclidiana entre dos posiciones (fila, col)."""
    return math.dist(a, b)


def chebyshev(a: Pos, b: Pos) -> float:
    """Distancia Chebyshev entre dos posiciones (fila, col)."""
    return float(max(abs(a[0] - b[0]), abs(a[1] - b[1])))


HEURISTICS: dict[str, HeuristicFn] = {
    "manhattan": manhattan,
    "euclidean": euclidean,
    "chebyshev": chebyshev,
}


@dataclass
class Grid:
    rows: int
    cols: int
    obstacles: set[Pos] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.rows < 1 or self.cols < 1:
            raise ValueError(f"Filas y columnas deben ser >= 1 (llegó {self.rows}x{self.cols}).")
        self.obstacles = {(r, c) for r, c in self.obstacles if self.in_bounds((r, c))}

    def in_bounds(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, pos: Pos) -> bool:
        return self.in_bounds(pos) and pos not in self.obstacles

    def neighbors(self, pos: Pos) -> list[Pos]:
        r, c = pos
        return [
            (r + dr, c + dc)
            for dr, dc in _MOVES_4
            if self.is_free((r + dr, c + dc))
        ]
