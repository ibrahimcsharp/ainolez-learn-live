---
title: Clear Instructions and Context
slug: clear-prompts
summary: Write prompts that say exactly what you want, for whom, and why.
minutes: 7
---
## Treat the model like a brilliant new colleague

An AI assistant knows a great deal but knows **nothing about your situation**: who the text is for, what you already tried, what "good" means to you. Most weak answers come from missing context, not a weak model.

A useful test: would a smart colleague who just joined understand your request without asking questions?

## Vague versus clear

**Vague:**

```
Write about our product.
```

**Clear:**

```
Write a 120-word description of our app "StudyBuddy" for the Google Play store.
Audience: university students who struggle to plan revision.
Main features: a revision timetable that adapts to exam dates, 25-minute focus timer,
progress streaks. Tone: friendly and direct, no hype words like "revolutionary".
End with one sentence inviting them to try it free.
```

The clear prompt states the **task**, **audience**, **content**, **tone**, **length** and **ending**.

## Say why

Reasons help the model make good choices you did not spell out. "Keep sentences short, because many readers are learning English" gets better results than "short sentences" alone.

## Say what to do, not only what to avoid

"Write in plain paragraphs" works better than "don't use bullet points". Describe the result you want.

## Give it a role when it helps

```
You are an experienced secondary-school chemistry teacher.
Explain covalent bonds to a 14-year-old using one everyday analogy.
```

A role sets vocabulary, depth and tone in one line.

## Building prompts in code

When you send prompts from a program, you build them from parts. Python's f-strings make that easy:

```python tryit
product = "StudyBuddy"
audience = "university students who struggle to plan revision"
words = 120

prompt = f"""Write a {words}-word store description of the app "{product}".
Audience: {audience}.
Tone: friendly and direct."""

print(prompt)
```

## Summary

- Give the context a newcomer would need.
- State task, audience, format, length and tone.
- Explain why, and describe what you want rather than what you don't.

```exercise
{
  "title": "A complete prompt",
  "prompt_md": "Use an f-string to build the prompt from the variables so the program prints exactly:\n```\nSummarise the article for busy managers in 3 bullet points.\n```",
  "starter_code": "audience = \"busy managers\"\npoints = 3\n\nprompt = \"\"\nprint(prompt)",
  "solution_code": "audience = \"busy managers\"\npoints = 3\n\nprompt = f\"Summarise the article for {audience} in {points} bullet points.\"\nprint(prompt)",
  "check_type": "output",
  "expected_value": "Summarise the article for busy managers in 3 bullet points.",
  "hint": "f\"Summarise the article for {audience} in {points} bullet points.\""
}
```

```quiz
[
  {"question": "What is the most common cause of a weak AI answer?", "options": ["Missing context in the prompt", "The model is too small", "Typing too slowly"], "answer": 0, "explanation": "The model only knows what you tell it about your situation."},
  {"question": "Which instruction usually works better?", "options": ["Write in flowing paragraphs", "Don't use bullet points", "No lists!!!"], "answer": 0, "explanation": "Describe the result you want."}
]
```
