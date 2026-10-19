---
title: Responsible AI
slug: responsible-ai
summary: Recognise bias, privacy and safety risks in AI systems and learn habits for using AI responsibly.
minutes: 8
---
## Why responsibility matters

AI systems make or influence decisions about loans, jobs, medical care and what news people see. Mistakes at that scale affect many people at once, so building and using AI responsibly is part of doing it well.

## Bias

A model learns the patterns in its data, including unfair ones. If past hiring data favoured one group, a model trained on it can repeat that.

```python tryit
# Approval rates in a (made-up) training set
applications = [
    ("group_a", True), ("group_a", True), ("group_a", False), ("group_a", True),
    ("group_b", False), ("group_b", True), ("group_b", False), ("group_b", False),
]

for group in ["group_a", "group_b"]:
    results = [ok for g, ok in applications if g == group]
    print(group, "approval rate:", sum(results) / len(results))
```

A model trained on this data would likely approve group A more often, even if the groups are equally qualified. Checking results per group, like this, is one of the first fairness tests.

## Privacy

- Do not paste passwords, personal data or secret company information into AI tools unless you know how the data is handled.
- Systems that train on personal data must follow laws such as the GDPR.

## Transparency and accountability

People should know when AI is used to make decisions about them, and a person should be responsible for the outcome. "The computer decided" is not an excuse.

## Safety and misuse

AI can be misused for scams, fake images and misinformation. AI developers add safeguards, and users should check sources, be careful with surprising claims and report misuse.

## Your checklist when using AI

1. **Verify**: check important facts and code.
2. **Protect**: keep personal and confidential data out.
3. **Disclose**: say when work is AI-assisted where it matters (school, journalism, research).
4. **Own it**: you are responsible for what you publish or submit.
5. **Learn**: use AI to understand, not only to copy. That is why this site's tutor explains instead of just giving answers.

## Summary

- Models can learn bias from data: test results per group.
- Protect privacy; be transparent; keep people accountable.
- Verify, protect, disclose, own and learn.

```exercise
{
  "title": "Rate per group",
  "prompt_md": "Complete `approval_rate(group)` to return the share of approved applications for that group. The program must print exactly:\n```\n0.75\n0.25\n```",
  "starter_code": "applications = [(\"a\", True), (\"a\", True), (\"a\", False), (\"a\", True),\n                (\"b\", False), (\"b\", True), (\"b\", False), (\"b\", False)]\n\ndef approval_rate(group):\n    pass\n\nprint(approval_rate(\"a\"))\nprint(approval_rate(\"b\"))",
  "solution_code": "applications = [(\"a\", True), (\"a\", True), (\"a\", False), (\"a\", True),\n                (\"b\", False), (\"b\", True), (\"b\", False), (\"b\", False)]\n\ndef approval_rate(group):\n    results = [ok for g, ok in applications if g == group]\n    return sum(results) / len(results)\n\nprint(approval_rate(\"a\"))\nprint(approval_rate(\"b\"))",
  "check_type": "output",
  "expected_value": "0.75\n0.25",
  "hint": "results = [ok for g, ok in applications if g == group]; return sum(results) / len(results)"
}
```

```quiz
{
  "title": "Final quiz: Introduction to AI",
  "final": true,
  "questions": [
    {"question": "Most modern AI is based on...", "options": ["Machine learning", "Hand-written rules only", "Quantum computers"], "answer": 0, "explanation": "Learning patterns from data."},
    {"question": "What does a model learn from in supervised learning?", "options": ["Labelled examples", "Random numbers", "Only its own output"], "answer": 0, "explanation": "Examples with known answers."},
    {"question": "What does training a neural network adjust?", "options": ["Weights", "The screen resolution", "The labels"], "answer": 0, "explanation": "Weights are nudged to reduce the error."},
    {"question": "A language model generates text...", "options": ["One token at a time", "By copying a database", "All at once from a template"], "answer": 0, "explanation": "Next-token prediction, repeated."},
    {"question": "How can a model become biased?", "options": ["It learns unfair patterns in its training data", "It chooses to be unfair", "Bias is impossible in computers"], "answer": 0, "explanation": "Models reflect their data."},
    {"question": "What should you do with an important fact from an AI answer?", "options": ["Verify it with a reliable source", "Publish it immediately", "Ask the same model again and trust it"], "answer": 0, "explanation": "Models can hallucinate."}
  ]
}
```
