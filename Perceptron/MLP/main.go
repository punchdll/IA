package main

import (
	neural "MLP/internal"
	"fmt"
	"os"
)

func main() {
	os.Exit(
		logic(),
	)
}

func logic() int {
	mlp := neural.CreateMLP().RandomizeNetwork()

	trainSet := [][]float64{
		{0, 0, 0},
		{0, 1, 1},
		{1, 0, 1},
	}

	mlp.Train(3_000_000, trainSet, 0.03)
	fmt.Println("Para [1, 1]:", mlp.Test([2]float64{1, 1}))
	return 0
}
