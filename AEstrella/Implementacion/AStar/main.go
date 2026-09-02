package main

import (
	"astar/core"
)

func main() {
	grid := core.NewGrid(3, 3)

	grid.SetOrigin(grid.SelectCell(0, 0))
	grid.SetDestination(grid.SelectCell(0, 2))

	// Bloquear celdas en forma de obstaculos
	grid.SelectCell(0, 1).Block()
	grid.SelectCell(1, 1).Block()

	grid.Play()

}
