# ASTAR

Implementación del algoritmo de búsqueda A*.

## Estructura

```text
.
├── main.py               # lanza el TUI
├── pyproject.toml        # proyecto uv (+ script astar-tui)
├── README.md
└── src/
    └── astar/
        ├── __init__.py       # API pública (reexporta grid + search)
        ├── grid.py           # Pos, Grid, heurísticas (manhattan/euclidean/chebyshev)
        ├── search.py         # SearchResult, astar_search, astar, grid_neighbors
        ├── state.py          # GridState, estado compartido por las dos interfaces
        ├── render.py         # render en texto plano de la grid
        ├── textual_app.py    # app Textual (launch_textual)
        ├── tui.py            # punto de entrada: run_tui / main
        └── py.typed
```

## Uso

```bash
uv sync
uv run main.py        # abre el menú TUI
# o instalado:
uv run astar-tui
```

Menú TUI (Textual, a pantalla completa):

- Grid navegable con el cursor: flechas o `WASD` para mover, `Espacio`
  alterna obstáculo (`#`), `Mayús+S` fija origen (`S`), `Mayús+G` fija
  destino (`G`), `Enter` ejecuta A*, `C` limpia obstáculos, `X` limpia camino.
- Click con el ratón mueve el cursor a la celda.
- Panel lateral: filas/columnas + botón «Nueva grid», selector de heurística
  (manhattan/euclidean/chebyshev), botones Ejecutar / Limpiar, y estadísticas
  del camino (`*` = camino).
- Atajos globales: `R` ejecutar, `C` limpiar obstáculos, `Q` salir.

