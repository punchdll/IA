from __future__ import annotations

from .grid import HEURISTICS
from .render import cell_char, path_cells
from .state import GridState

__all__ = ["launch_textual"]

CELL_W = 3  # ancho en caracteres de cada celda en el widget


def _cell_style(
    state: GridState, pos: tuple[int, int], is_cursor: bool, path: set[tuple[int, int]]
) -> str:
    if pos == state.start:
        base = "bold white on dark_green"
    elif pos == state.goal:
        base = "bold white on dark_red"
    elif pos in state.obstacles:
        base = "grey50 on black"
    elif pos in path:
        base = "bold yellow"
    else:
        base = ""
    if is_cursor:
        base = (base + " reverse").strip()
    return base


def launch_textual():
    from rich.text import Text
    from textual import events
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Horizontal, Vertical, ScrollableContainer
    from textual.widgets import Button, Footer, Header, Input, Label, Select, Static

    class GridView(Static, can_focus=True):
        def __init__(self, state: GridState, **kwargs):
            super().__init__(**kwargs)
            self.state = state
            self.cursor: tuple[int, int] = state.start or (0, 0)

        def clamp_cursor(self):
            r, c = self.cursor
            r = max(0, min(self.state.rows - 1, r))
            c = max(0, min(self.state.cols - 1, c))
            self.cursor = (r, c)

        def render(self):
            self.clamp_cursor()
            path = path_cells(self.state)
            t = Text()
            for r in range(self.state.rows):
                for c in range(self.state.cols):
                    pos = (r, c)
                    ch = cell_char(self.state, pos, path)
                    style = _cell_style(self.state, pos, pos == self.cursor, path)
                    t.append(f" {ch} ", style=style)
                if r < self.state.rows - 1:
                    t.append("\n")
            return t

        def move(self, dr: int, dc: int):
            r, c = self.cursor
            self.cursor = (max(0, min(self.state.rows - 1, r + dr)),
                           max(0, min(self.state.cols - 1, c + dc)))
            self.refresh()
            self.app.update_info()

        def on_key(self, event: events.Key) -> None:
            k = event.key
            if k in ("up", "w"):
                self.move(-1, 0)
            elif k in ("down", "s"):
                self.move(1, 0)
            elif k in ("left", "a"):
                self.move(0, -1)
            elif k in ("right", "d"):
                self.move(0, 1)
            elif k == "space":
                try:
                    self.state.toggle_obstacle(self.cursor)
                except ValueError as exc:
                    self.app.flash(str(exc))
                self.refresh()
                self.app.update_info()
            elif k == "S":
                self.state.set_start(self.cursor)
                self.refresh()
                self.app.update_info()
            elif k == "G":
                self.state.set_goal(self.cursor)
                self.refresh()
                self.app.update_info()
            elif k == "enter":
                self.app.run_search()
            elif k in ("c", "C"):
                self.app.clear_obstacles()
            elif k in ("x", "X"):
                self.app.clear_path()
            else:
                return
            event.prevent_default()
            event.stop()

        async def on_click(self, event: events.Click) -> None:
            try:
                col = int(event.offset.x) // CELL_W
                row = int(event.offset.y)
            except Exception:
                return
            if self.state.in_bounds(row, col):
                self.cursor = (row, col)
                self.refresh()
                self.app.update_info()
                self.focus()

    class AStarApp(App):
        CSS = """
        #grid-col {
            width: 1fr;
            height: 1fr;
            align: center middle;
        }
        #side {
            width: 100;
            height: 1fr;
            border: solid grey;
            padding: 0 1;
            align-horizontal: center;
            overflow-y: auto;
        }
        GridView {
            border: solid grey;
            padding: 1;
            height: auto;
            width: auto;
        }
        .section {
            border: solid grey;
            padding: 1;
            margin: 0 0 1 0;
            width: 100%;
            align: center middle;
        }
        .section-title {
            color: $text-accent;
            text-style: bold;
            margin: 0 0 1 0;
            text-align: center;
        }
        .section Label {
            text-align: center;
            text-wrap: wrap;
            overflow: hidden;
        }
        .section Input {
            width: 30%;
            margin: 0 1;
        }
        .section Button {
            width: auto;
            margin: 0 1;
        }
        .section Select {
            width: 80%;
            margin: 0;
        }
        .section Horizontal {
            align: center middle;
            height: auto;
        }
        #stats {
            color: $text-success;
            text-style: bold;
        }
        #msg {
            color: yellow;
        }
        #help {
            color: grey;
        }
        #main-row {
            height: 1fr;
        }
        """
        BINDINGS = [
            Binding("q", "quit", "Salir"),
            Binding("r", "run", "Ejecutar A*"),
            Binding("c", "clear_obs", "Limpiar obstáculos"),
        ]

        def __init__(self):
            super().__init__()
            self.state = GridState()

        def compose(self) -> ComposeResult:
            yield Header(show_clock=False)
            with Horizontal(id="main-row"):
                with Vertical(id="grid-col"):
                    yield GridView(self.state, id="grid")
                    yield Label("", id="pos")
                with Vertical(id="side"):
                    with Vertical(classes="section"):
                        yield Label("[b]Dimensiones[/b]", classes="section-title")
                        with Horizontal():
                            yield Input(value=str(self.state.rows), id="in-rows")
                            yield Input(value=str(self.state.cols), id="in-cols")
                            yield Button("Nueva grid", id="btn-grid")
                    with Vertical(classes="section"):
                        yield Label("[b]Heurística[/b]", classes="section-title")
                        yield Select(
                            [(n, n) for n in HEURISTICS],
                            value=self.state.heuristic_name,
                            id="sel-h",
                        )
                    with Vertical(classes="section"):
                        yield Label("[b]Acciones[/b]", classes="section-title")
                        with Horizontal():
                            yield Button("Ejecutar A* (Enter)", variant="primary", id="btn-run")
                            yield Button("Limpiar obstáculos (C)", id="btn-clear-obs")
                            yield Button("Limpiar camino (X)", id="btn-clear-path")
                    with Vertical(classes="section"):
                        yield Label("[b]Info[/b]", classes="section-title")
                        yield Label("", id="stats")
                        yield Label("", id="msg")
                    yield Label(
                        "[b]Grid:[/b] flechas/WASD mover · Espacio obstáculo · "
                        "Mayús+S origen · Mayús+G destino · Enter buscar · "
                        "Click mueve cursor",
                        id="help",
                    )
            yield Footer()

        def on_mount(self):
            self.update_info()
            self.query_one(GridView).focus()

        def grid(self) -> GridView:
            return self.query_one(GridView)

        def flash(self, msg: str):
            self.query_one("#msg", Label).update(msg)

        def update_info(self):
            st = self.state
            g = self.grid()
            try:
                self.query_one("#pos", Label).update(
                    f"Cursor={g.cursor}  S={st.start} G={st.goal}  "
                    f"#{len(st.obstacles)} obstáculos  h={st.heuristic_name}"
                )
                path_txt = ""
                if st.path:
                    path_txt = f"Camino: {len(st.path)} celdas, {len(st.path) - 1} pasos."
                self.query_one("#stats", Label).update(
                    f"Grid {st.rows}x{st.cols}\n{path_txt}"
                    + (f"\n{st.last_msg}" if st.last_msg else "")
                )
            except Exception:
                pass

        def run_search(self):
            try:
                result = self.state.run()
            except ValueError as exc:
                self.flash(str(exc))
                return
            self.flash(result.describe() + (f"  Ruta: {result.path}" if result.path else ""))
            self.grid().refresh(layout=True)
            self.update_info()
            self.grid().focus()

        def clear_obstacles(self):
            self.state.clear_obstacles()
            self.grid().refresh(layout=True)
            self.update_info()

        def clear_path(self):
            self.state.clear_path()
            self.grid().refresh(layout=True)
            self.update_info()

        def action_run(self):
            self.run_search()

        def action_clear_obs(self):
            self.clear_obstacles()

        def on_button_pressed(self, event: Button.Pressed):
            bid = event.button.id
            if bid == "btn-run":
                self.run_search()
            elif bid == "btn-clear-obs":
                self.clear_obstacles()
            elif bid == "btn-clear-path":
                self.clear_path()
            elif bid == "btn-grid":
                try:
                    rows = max(1, min(30, int(self.query_one("#in-rows", Input).value or 5)))
                    cols = max(1, min(30, int(self.query_one("#in-cols", Input).value or 5)))
                except ValueError:
                    self.flash("Filas/columnas deben ser números.")
                    return
                self.state.resize(rows, cols)
                if self.state.start is None:
                    self.state.start = (0, 0)
                if self.state.goal is None:
                    self.state.goal = (rows - 1, cols - 1)
                self.grid().cursor = self.state.start or (0, 0)
                self.flash(f"Grid {rows}x{cols} creada.")
                self.grid().refresh(layout=True)
                self.update_info()
                self.grid().focus()

        def on_select_changed(self, event: Select.Changed):
            if event.select.id == "sel-h":
                self.state.heuristic_name = str(event.value)
                self.state.clear_path()
                self.grid().refresh(layout=True)
                self.update_info()

    return AStarApp
