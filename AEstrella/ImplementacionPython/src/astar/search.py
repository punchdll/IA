from __future__ import annotations

import heapq
import itertools
import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from .grid import HEURISTICS, Grid, HeuristicFn, Pos

__all__ = ["SearchResult", "astar_search", "astar", "grid_neighbors"]

CostFn = Callable[[Pos, Pos], float]
NeighborsFn = Callable[[Pos], Iterable[Pos]]


@dataclass
class SearchResult:
    path: list[Pos] | None
    expanded: int = 0

    @property
    def found(self) -> bool:
        return self.path is not None

    @property
    def steps(self) -> int | None:
        return None if self.path is None else len(self.path) - 1

    def describe(self) -> str:
        if self.path is None:
            return "Sin camino."
        return (
            f"Camino encontrado: {len(self.path)} celdas "
            f"({self.steps} pasos, {self.expanded} nodos expandidos)."
        )


def _resolve_cost(cost: float | CostFn) -> CostFn:
    if callable(cost):
        def cost_fn(a: Pos, b: Pos) -> float:
            value = float(cost(a, b))
            if value < 0:
                raise ValueError(f"El coste no puede ser negativo (llegó {value}).")
            return value

        return cost_fn
    if cost < 0:
        raise ValueError(f"El coste no puede ser negativo (llegó {cost}).")
    value = float(cost)
    return lambda a, b: value


def _resolve_heuristic(heuristic: str | HeuristicFn) -> HeuristicFn:
    if callable(heuristic):
        return heuristic
    try:
        return HEURISTICS[heuristic]
    except KeyError:
        raise ValueError(
            f"Heurística desconocida: {heuristic!r}. Elige entre {sorted(HEURISTICS)}."
        ) from None


def astar_search(
    start: Pos,
    goal: Pos,
    neighbors_fn: NeighborsFn,
    *,
    cost: float | CostFn = 1.0,
    heuristic: str | HeuristicFn = "manhattan",
) -> SearchResult:
    cost_fn = _resolve_cost(cost)
    heuristic_fn = _resolve_heuristic(heuristic)

    tiebreak = itertools.count()
    open_heap: list[tuple[float, float, int, Pos]] = []
    heapq.heappush(open_heap, (heuristic_fn(start, goal), 0.0, next(tiebreak), start))
    g_score: dict[Pos, float] = {start: 0.0}
    came_from: dict[Pos, Pos] = {}
    expanded = 0

    while open_heap:
        _, g, _, current = heapq.heappop(open_heap)
        if g > g_score.get(current, math.inf):
            continue
        expanded += 1
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return SearchResult(path=list(reversed(path)), expanded=expanded)

        for nxt in neighbors_fn(current):
            new_g = g_score[current] + cost_fn(current, nxt)
            if new_g < g_score.get(nxt, math.inf):
                g_score[nxt] = new_g
                came_from[nxt] = current
                heapq.heappush(
                    open_heap,
                    (new_g + heuristic_fn(nxt, goal), new_g, next(tiebreak), nxt),
                )
    return SearchResult(path=None, expanded=expanded)


def astar(
    start: Pos,
    goal: Pos,
    neighbors_fn: NeighborsFn,
    *,
    cost: float | CostFn = 1.0,
    heuristic: str | HeuristicFn = "manhattan",
) -> list[Pos] | None:
    return astar_search(
        start, goal, neighbors_fn, cost=cost, heuristic=heuristic
    ).path


def grid_neighbors(
    rows: int, cols: int, obstacles: Iterable[Pos] = ()
) -> NeighborsFn:
    return Grid(rows, cols, set(obstacles)).neighbors
