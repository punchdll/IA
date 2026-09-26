
from __future__ import annotations

from .grid import Grid, Pos
from .search import SearchResult, astar_search

__all__ = ["GridState"]


class GridState:
    def __init__(self, rows=5, cols=5):
        self.grid = Grid(rows, cols)
        self.start: Pos | None = (0, 0)
        self.goal: Pos | None = (rows - 1, cols - 1)
        self.heuristic_name = "manhattan"
        self.path: list[Pos] | None = None
        self.last_msg = ""
        self.expanded = 0

    @property
    def rows(self):
        return self.grid.rows

    @property
    def cols(self):
        return self.grid.cols

    @property
    def obstacles(self):
        return self.grid.obstacles

    def in_bounds(self, r, c):
        return self.grid.in_bounds((r, c))

    def resize(self, rows, cols):
        self.grid = Grid(rows, cols, set(self.grid.obstacles))
        if self.start and not self.in_bounds(*self.start):
            self.start = None
        if self.goal and not self.in_bounds(*self.goal):
            self.goal = None
        self.path = None

    def toggle_obstacle(self, pos):
        if pos == self.start or pos == self.goal:
            raise ValueError("No puede haber obstáculo en origen/destino.")
        self.grid.obstacles.symmetric_difference_update({pos})
        self.path = None

    def set_start(self, pos):
        self.grid.obstacles.discard(pos)
        self.start = pos
        self.path = None

    def set_goal(self, pos):
        self.grid.obstacles.discard(pos)
        self.goal = pos
        self.path = None

    def clear_obstacles(self):
        self.grid.obstacles.clear()
        self.path = None

    def clear_path(self):
        self.path = None

    def run(self) -> SearchResult:
        if self.start is None or self.goal is None:
            raise ValueError("Falta origen o destino.")
        if self.start in self.grid.obstacles or self.goal in self.grid.obstacles:
            raise ValueError("Origen/destino no puede estar en un obstáculo.")
        result = astar_search(
            self.start, self.goal, self.grid.neighbors, heuristic=self.heuristic_name
        )
        self.path = result.path
        self.expanded = result.expanded
        self.last_msg = result.describe()
        return result
