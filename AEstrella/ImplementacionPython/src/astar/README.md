# A* — Implementación

## Estructura

```
src/astar/
├── grid.py        # Representación de la cuadrícula y heurísticas
├── search.py      # Algoritmo A*
├── state.py       # Estado de la app (origen, destino, obstáculos, path)
├── render.py      # Renderizado en texto plano
├── textual_app.py # Interfaz TUI con Textual
├── tui.py         # Punto de entrada run_tui()
└── __init__.py
```

## Lógica

### grid.py
- `Grid` (dataclass): dimensiones `rows x cols` + conjunto de obstáculos.
- Vecindad de 4 direcciones (arriba, abajo, izquierda, derecha).
- Tres heurísticas: `manhattan`, `euclidean`, `chebyshev`.

### search.py
- `astar_search(start, goal, neighbors_fn, cost, heuristic) -> SearchResult`
- Cola de prioridad (`heapq`) con `f = g + h` y contador de desempate.
- `g_score`: costo acumulado desde el origen.
- `came_from`: reconstrucción del camino al llegar al meta.
- Devuelve `SearchResult(path, expanded)`; `path=None` si no hay ruta.

### state.py
- `GridState`: envuelve `Grid` con `start`, `goal`, `heuristic_name`, `path`.
- Cualquier mutación invalida el path almacenado (`self.path = None`).
- `run()` invoca `astar_search` y guarda el resultado.

### textual_app.py
- `GridView` (Static): captura teclado (WASD/flechas, espacio, S, G, Enter) y click.
- `AStarApp`: layout con grid a la izquierda y panel de controles a la derecha.
- `refresh(layout=True)` fuerza re-layout al cambiar dimensiones del grid.
