---
title: Neural Networks
slug: neural-networks
summary: See how an artificial neuron works, how networks learn by adjusting weights, and why deep learning took off.
minutes: 9
---
## An artificial neuron

A neuron takes inputs, multiplies each by a **weight**, adds them with a **bias**, and passes the total through an **activation function**:

```python tryit
import math

def neuron(inputs, weights, bias):
    total = sum(x * w for x, w in zip(inputs, weights)) + bias
    return 1 / (1 + math.exp(-total))     # sigmoid: squashes to 0..1

# Should I take an umbrella? inputs: [cloudy (0/1), rain forecast (0..1)]
weights = [1.5, 4.0]
bias = -2.5
print(round(neuron([1, 0.9], weights, bias), 2))   # cloudy, rain likely
print(round(neuron([0, 0.1], weights, bias), 2))   # clear sky
```

The weights decide how much each input matters. Learning means finding good weights.

## Learning: nudge the weights

Training repeats a simple loop:

1. Make a prediction.
2. Measure the **error** (how wrong it was).
3. Nudge each weight a little in the direction that reduces the error (**gradient descent**).

```python tryit
# Learn y = 2x + 1 from examples with one weight and one bias
data = [(1, 3), (2, 5), (3, 7), (4, 9)]
w, b, rate = 0.0, 0.0, 0.05

for step in range(500):
    for x, y in data:
        error = (w * x + b) - y
        w -= rate * error * x
        b -= rate * error

print(f"learned w={w:.2f}, b={b:.2f}")
print("prediction for x=10:", round(w * 10 + b, 1))
```

The program was never told "2" or "1": it found them by reducing its error, step by step.

## Layers and deep learning

A **neural network** connects many neurons in layers: an input layer, one or more hidden layers and an output layer. "Deep" learning means many layers. Each layer learns more abstract features: in an image model, early layers find edges, later layers find eyes and wheels.

Deep learning took off around 2012 because three things came together: huge datasets, fast GPUs and better training methods.

## What neural networks power

- Image recognition and medical scan analysis.
- Speech recognition and translation.
- Large language models such as Claude (next lesson).

## Summary

- A neuron: weighted sum + bias → activation.
- Training adjusts weights to reduce the error (gradient descent).
- Deep networks stack many layers that learn features automatically.

```exercise
{
  "title": "Weighted sum",
  "prompt_md": "Complete `weighted_sum` to return the sum of each input times its weight, plus the bias. The program must print exactly `3.5`",
  "starter_code": "def weighted_sum(inputs, weights, bias):\n    pass\n\nprint(weighted_sum([1, 2], [0.5, 1.0], 1))",
  "solution_code": "def weighted_sum(inputs, weights, bias):\n    return sum(x * w for x, w in zip(inputs, weights)) + bias\n\nprint(weighted_sum([1, 2], [0.5, 1.0], 1))",
  "check_type": "output",
  "expected_value": "3.5",
  "hint": "sum(x * w for x, w in zip(inputs, weights)) + bias"
}
```

```quiz
[
  {"question": "What does training a neural network change?", "options": ["Its weights and biases", "Its programming language", "The training data"], "answer": 0, "explanation": "Learning = adjusting weights to reduce error."},
  {"question": "What does 'deep' mean in deep learning?", "options": ["Many layers of neurons", "Very long training", "Underwater robots"], "answer": 0, "explanation": "Deep networks have many hidden layers."}
]
```
