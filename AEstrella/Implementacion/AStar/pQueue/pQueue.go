package pQueue

import "errors"

type PriorityFunction func(a, b int) bool

var errEmpty = errors.New("priority queue is empty")

type PriorityQueue[T any] struct {
	heap              []*entry[T]
	hasHigherPriority PriorityFunction
}

type entry[T any] struct {
	value    T
	priority int
}

func New[T any](priorityFunction PriorityFunction) *PriorityQueue[T] {
	return &PriorityQueue[T]{
		heap:              make([]*entry[T], 0),
		hasHigherPriority: priorityFunction}
}

func NewMin[T any]() *PriorityQueue[T] {
	return New[T](
		func(a, b int) bool {
			return a < b
		},
	)
}

func NewMax[T any]() *PriorityQueue[T] {
	return New[T](func(a, b int) bool {
		return a > b
	})
}

func (q *PriorityQueue[T]) Push(value T, priority int) {
	q.heap = append(q.heap, &entry[T]{value: value, priority: priority})

	for currentNodeIndex := len(q.heap) - 1; currentNodeIndex > 0; {
		parentIndex := (currentNodeIndex - 1) / 2
		if !q.hasHigherPriority(q.heap[currentNodeIndex].priority, q.heap[parentIndex].priority) {
			break
		}
		q.heap[parentIndex], q.heap[currentNodeIndex] = q.heap[currentNodeIndex], q.heap[parentIndex]

		currentNodeIndex = parentIndex
	}
}

func (q *PriorityQueue[T]) Empty() bool {
	if len(q.heap) == 0 {
		return true
	}
	return false
}

func (q *PriorityQueue[T]) Pop() (T, int, error) {

	if len(q.heap) == 0 {
		return *new(T), 0, errEmpty
	}

	root := q.heap[0]

	if len(q.heap) == 1 {
		q.heap = q.heap[:0]
		return root.value, root.priority, nil
	}

	q.heap[0] = q.heap[len(q.heap)-1]
	q.heap = q.heap[:len(q.heap)-1]

	for currentNodeIndex := 0; ; {

		leftNodeIndex := 2*currentNodeIndex + 1
		rightNodeIndex := 2*currentNodeIndex + 2
		highestPriorityNodeIndex := currentNodeIndex

		if leftNodeIndex < len(q.heap) &&
			q.hasHigherPriority(q.heap[leftNodeIndex].priority, q.heap[highestPriorityNodeIndex].priority) {
			highestPriorityNodeIndex = leftNodeIndex
		}

		if rightNodeIndex < len(q.heap) &&
			q.hasHigherPriority(q.heap[rightNodeIndex].priority, q.heap[highestPriorityNodeIndex].priority) {
			highestPriorityNodeIndex = rightNodeIndex

		}

		if highestPriorityNodeIndex == currentNodeIndex {
			break
		}

		q.heap[currentNodeIndex], q.heap[highestPriorityNodeIndex] = q.heap[highestPriorityNodeIndex], q.heap[currentNodeIndex]

		currentNodeIndex = highestPriorityNodeIndex
	}

	return root.value, root.priority, nil
}
