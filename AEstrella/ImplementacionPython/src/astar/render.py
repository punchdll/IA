
from __future__ import annotations

from .grid import Pos
from .state import GridState

__all__ = [
    "CELDA_LIBRE",
    "CELDA_OBSTACULO",
    "CELDA_ORIGEN",
    "CELDA_DESTINO",
    "CELDA_CAMINO",
    "path_cells",
    "cell_char",
    "render",
]

CELDA_LIBRE = "."
CELDA_OBSTACULO = "#"
CELDA_ORIGEN = "S"
CELDA_DESTINO = "G"
CELDA_CAMINO = "*"


def path_cells(state: GridState, show_path: bool = True) -> set[Pos]:
    if show_path and state.path:
        return set(state.path)
    return set()


def cell_char(state: GridState, pos: Pos, path: set[Pos]) -> str:
    if pos == state.start:
        return CELDA_ORIGEN
    if pos == state.goal:
        return CELDA_DESTINO
    if pos in state.obstacles:
        return CELDA_OBSTACULO
    if pos in path:
        return CELDA_CAMINO
    return CELDA_LIBRE


def render(state: GridState, cursor: Pos | None = None, show_path: bool = True) -> str:
    path = path_cells(state, show_path)
    lines = ["    " + " ".join(f"{c:2d}" for c in range(state.cols))]
    for r in range(state.rows):
        cells = []
        for c in range(state.cols):
            pos = (r, c)
            ch = cell_char(state, pos, path)
            cells.append(f"[{ch}]" if cursor == pos else f" {ch} ")
        lines.append(f"{r:2d} " + "".join(cells))
    return "\n".join(lines)
