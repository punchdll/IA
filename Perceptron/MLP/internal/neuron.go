package internal

import (
	"fmt"
	"math"
	"math/rand"

	humanize "github.com/dustin/go-humanize"
)

type neuron struct {
	weights    [2]float64
	bias       float64
	delta      float64
	activation float64
}

type MLP struct {
	hiddenLayer  [2]neuron
	outputLayer  neuron
	networkError float64
}

func CreateMLP() *MLP {
	return &MLP{
		hiddenLayer: [2]neuron{
			{weights: [2]float64{getRandomNumber(), getRandomNumber()},
				bias:       0,
				delta:      0,
				activation: 0,
			},
			{weights: [2]float64{getRandomNumber(), getRandomNumber()},
				bias:       0,
				delta:      0,
				activation: 0,
			},
		},
		outputLayer: neuron{
			weights:    [2]float64{getRandomNumber(), getRandomNumber()},
			bias:       0,
			delta:      0,
			activation: 0,
		},
		networkError: 0,
	}
}

func (n *neuron) randomizeNeuron() {
	for index := 0; index < len(n.weights); index++ {
		n.weights[index] = getRandomNumber()
	}
	n.bias = getRandomNumber()
}

func (m *MLP) RandomizeNetwork() *MLP {
	for index := range len(m.hiddenLayer) {
		m.hiddenLayer[index].randomizeNeuron()
	}
	m.outputLayer.randomizeNeuron()

	return m
}

func sigmoid(input float64) float64 {
	return 1.0 / (1.0 + math.Exp(-input))
}

func getRandomNumber() float64 {
	return float64(rand.Int()) / float64(math.MaxInt)
}

func (n *neuron) computePreactivation(sample [2]float64) *neuron {
	n.activation = n.weights[0]*sample[0] + n.weights[1]*sample[1] + n.bias
	return n
}

func (n *neuron) activate() *neuron {
	n.activation = sigmoid(n.activation)
	return n
}

func (m *MLP) Test(features [2]float64) float64 {

	for neuronIndex := range m.hiddenLayer {
		m.hiddenLayer[neuronIndex].
			computePreactivation(features).
			activate()
	}

	return m.outputLayer.
		computePreactivation(
			[2]float64{
				m.hiddenLayer[0].activation,
				m.hiddenLayer[1].activation,
			},
		).
		activate().activation
}

func (m *MLP) __train(sample [3]float64, learningRate float64) *MLP {

	label := sample[2]
	features := [2]float64(sample[:len(sample)-1])

	for neuronIndex := range len(m.hiddenLayer) {
		m.hiddenLayer[neuronIndex].computePreactivation(features).activate()
	}

	m.outputLayer.computePreactivation(
		[2]float64{
			m.hiddenLayer[0].activation,
			m.hiddenLayer[1].activation,
		},
	).activate()

	m.networkError = label - m.outputLayer.activation

	m.outputLayer.delta = m.networkError * m.outputLayer.activation * (1 - m.outputLayer.activation)

	for index := range len(m.hiddenLayer) {
		m.hiddenLayer[index].delta = m.outputLayer.delta * m.outputLayer.weights[index] * m.hiddenLayer[index].activation * (1 - m.hiddenLayer[index].activation)
	}

	for index := range len(m.outputLayer.weights) {
		m.outputLayer.weights[index] += learningRate * m.outputLayer.delta * m.hiddenLayer[index].activation
	}

	m.outputLayer.bias += learningRate * m.outputLayer.delta

	for neuronIndex := range len(m.hiddenLayer) {
		for weightIndex := range len(m.hiddenLayer[neuronIndex].weights) {
			m.hiddenLayer[neuronIndex].weights[weightIndex] += learningRate * m.hiddenLayer[neuronIndex].delta * features[weightIndex]
		}
		m.hiddenLayer[neuronIndex].bias += learningRate * m.hiddenLayer[neuronIndex].delta
	}

	return m
}

func (m *MLP) Train(epochs int64, dataset [][]float64, learningRate float64) *MLP {

	for epoch := range epochs {
		var epochError float64

		for _, sample := range dataset {
			m.__train([3]float64(sample), learningRate)

			epochError += math.Abs(m.networkError)
		}

		epochError /= float64(len(dataset))

		fmt.Printf(
			"\r\033[KEpoch: %s (%s remaining) %d%% | Error: %.10f",
			humanize.Comma(epoch+1),
			humanize.Comma(epochs-(epoch+1)),
			int64((float64(epoch+1)/float64(epochs))*100),
			epochError,
		)
	}

	fmt.Println()
	return m
}
