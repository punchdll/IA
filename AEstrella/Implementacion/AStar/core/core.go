package core

import (
	"astar/pQueue"
	"fmt"
	"math"
	"strconv"
)

type node struct {
	x         int
	y         int
	g         int
	h         int
	f         int
	parent    *node
	isBlocked bool
}

func (n *node) String() string {
	return "(" + strconv.Itoa(n.x) + ", " + strconv.Itoa(n.y) + ")"
}

const (
	diagonalCost = 15
	linealCost   = 10
)

type Grid struct {
	nodes       [][]node
	origin      *node
	destination *node
}

func NewGrid(width, height int) Grid {
	grid := Grid{
		nodes: make([][]node, height),
	}

	for y := 0; y < height; y++ {
		grid.nodes[y] = make([]node, width)

		for x := 0; x < width; x++ {
			grid.nodes[y][x] = node{
				x: x,
				y: y,
			}
		}
	}

	return grid
}

func (g *Grid) SelectCell(x, y int) *node {
	return &g.nodes[y][x]
}

func (g *Grid) Neighbors(c *node) []*node {
	neighbors := make([]*node, 0, 8)

	directions := [][2]int{
		{0, -1},
		{1, -1},
		{1, 0},
		{1, 1},
		{0, 1},
		{-1, 1},
		{-1, 0},
		{-1, -1},
	}

	for _, direction := range directions {
		x := c.x + direction[0]
		y := c.y + direction[1]

		if y < 0 || y >= len(g.nodes) {
			continue
		}

		if x < 0 || x >= len(g.nodes[y]) {
			continue
		}

		neighbor := &g.nodes[y][x]

		if !neighbor.isBlocked {
			neighbors = append(neighbors, neighbor)
		}
	}

	return neighbors
}

func absInt(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func heuristic(a, b node) int {
	return int(math.Abs(float64(b.x-a.x)) + math.Abs(float64(b.y-a.y)))
}

func (p *node) fullCost(neighbor *node, destination node) int {
	stepCost := p.stepCostTo(neighbor)

	neighbor.parent = p
	neighbor.g = p.g + stepCost
	neighbor.h = heuristic(*neighbor, destination)
	neighbor.f = neighbor.g + neighbor.h

	return neighbor.f
}

func (p *node) stepCostTo(neighbor *node) int {
	if neighbor.x != p.x && neighbor.y != p.y {
		return diagonalCost
	}
	return linealCost
}

func (n *node) hasBetterPath(parent *node, newG int) bool {
	return n.parent != nil && n.g <= newG
}

func (c *node) Block() {
	c.isBlocked = true
}

func (g *Grid) SetOrigin(origin *node) {
	g.origin = origin
}

func (g *Grid) SetDestination(destination *node) {
	g.destination = destination
}

func (g *Grid) Play() {
	if g.origin == nil || g.destination == nil {
		return
	}

	openList := pQueue.NewMin[node]()
	closedSet := make(map[[2]int]bool)

	g.origin.g = 0
	g.origin.h = heuristic(*g.origin, *g.destination)
	g.origin.f = g.origin.h
	g.origin.parent = nil
	openList.Push(*g.origin, g.origin.f)

	for !openList.Empty() {
		current, _, _ := openList.Pop()

		key := [2]int{current.x, current.y}
		if closedSet[key] {
			continue
		}

		closedSet[key] = true

		fmt.Println(current.String(), "Costo:", current.g)

		if current.x == g.destination.x && current.y == g.destination.y {
			return
		}

		for _, neighbor := range g.Neighbors(&current) {
			nKey := [2]int{neighbor.x, neighbor.y}
			if closedSet[nKey] {
				continue
			}

			if neighbor.hasBetterPath(&current, current.g+current.stepCostTo(neighbor)) {
				continue
			}

			cost := current.fullCost(neighbor, *g.destination)
			openList.Push(*neighbor, cost)
		}
	}
}
