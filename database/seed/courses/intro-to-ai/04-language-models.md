---
title: How Chatbots Work
slug: language-models
summary: Understand tokens, next-token prediction, training and why language models sometimes make things up.
minutes: 9
---
## Large language models

Chat assistants such as Claude are built on **large language models (LLMs)**: very large neural networks trained on huge amounts of text to predict what comes next.

## Tokens

Models read and write **tokens**: pieces of words. "unbelievable" might be "un", "believ", "able". A rough rule for English: 1 token ≈ ¾ of a word. Prices and limits of AI services are counted in tokens.

## Predicting the next token

At its core, a language model answers one question again and again: *given the text so far, what token is likely next?* Here is a tiny version that learns which word follows which:

```python tryit
import random
from collections import defaultdict

text = """the cat sat on the mat . the dog sat on the rug .
the cat saw the dog . the dog saw the cat ."""

following = defaultdict(list)
words = text.split()
for current, nxt in zip(words, words[1:]):
    following[current].append(nxt)

print("after 'the':", following["the"])

random.seed(4)
word, sentence = "the", ["the"]
for _ in range(8):
    word = random.choice(following[word])
    sentence.append(word)
print(" ".join(sentence))
```

A real LLM looks at thousands of previous tokens, not one word, and has learned grammar, facts, reasoning patterns and styles from its training. But it still generates one token at a time.

## From text predictor to assistant

1. **Pre-training**: learn to predict text from a very large dataset.
2. **Fine-tuning**: train further on examples of helpful conversations.
3. **Feedback training**: people and AI feedback rate answers, teaching the model to be helpful, honest and harmless.

## Why models make mistakes

A model produces likely-sounding text. When it lacks the facts, it can produce a confident, wrong answer: a **hallucination**. Good habits:

- Check important facts against reliable sources.
- Give the model the documents it needs (this site's AI tutor reads the lesson you are on).
- Ask it to say when it is unsure.

## The context window

The **context window** is how much text a model can consider at once: your question, earlier messages and any documents. Modern models handle long documents, but they only "know" what is in their training and their context.

## Summary

- LLMs predict the next token, one at a time.
- Pre-training, fine-tuning and feedback turn a predictor into an assistant.
- Models can hallucinate: verify important facts.

```exercise
{
  "title": "Count the followers",
  "prompt_md": "Count how many times each word appears **right after** the word `the`, and print the counts as a dictionary sorted by word. The output must be exactly `{'cat': 2, 'dog': 1, 'mat': 1}`",
  "starter_code": "words = \"the cat sat on the mat and the cat saw the dog\".split()\n\n",
  "solution_code": "words = \"the cat sat on the mat and the cat saw the dog\".split()\n\ncounts = {}\nfor current, nxt in zip(words, words[1:]):\n    if current == \"the\":\n        counts[nxt] = counts.get(nxt, 0) + 1\nprint(dict(sorted(counts.items())))",
  "check_type": "output",
  "expected_value": "{'cat': 2, 'dog': 1, 'mat': 1}",
  "hint": "Loop over zip(words, words[1:]) and count nxt when current == \"the\"."
}
```

```quiz
[
  {"question": "What does a language model predict?", "options": ["The next token", "The user's location", "The correct answer, always"], "answer": 0, "explanation": "It generates text one token at a time."},
  {"question": "What is a hallucination?", "options": ["A confident answer that is false", "A picture the model draws", "A very long answer"], "answer": 0, "explanation": "Likely-sounding text is not always true."}
]
```
