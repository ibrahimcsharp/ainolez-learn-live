---
title: Testing and Improving Prompts
slug: iterate
summary: Improve prompts systematically with test cases, and reduce made-up answers.
minutes: 7
---
## Prompts are code: test them

A prompt that works once may fail on the next input. Treat prompts like code:

1. Write down what a good answer looks like.
2. Collect **test cases**: typical inputs and tricky ones.
3. Run the prompt on all of them and check the results.
4. Change **one thing** at a time and run the tests again.

## Automatic checks

Simple checks catch many problems without reading every answer:

```python tryit
answers = {
    "refund": "Your refund of $20 was sent today and arrives in 3-5 days.",
    "late parcel": "So sorry! Your parcel is on its way.",
    "angry": "Calm down.",
}

def check(answer):
    problems = []
    if len(answer.split()) > 40:
        problems.append("too long")
    if "calm down" in answer.lower():
        problems.append("rude phrase")
    if not answer.rstrip().endswith((".", "!")):
        problems.append("no full stop")
    return problems

for case, answer in answers.items():
    print(f"{case:12} {check(answer) or 'ok'}")
```

For qualities that are hard to code (helpfulness, tone), a person or a second model can grade answers against a short checklist.

## Reducing made-up answers

- Give the model the source documents and say: *answer only from these; if the answer is not there, say you don't know*.
- Ask for quotes or references from the sources.
- Allow "I'm not sure" as a good answer.

## When the result is wrong, ask why

Read the bad answer and ask what the model was missing. Usually the fix is more context, a clearer goal or an example, not shouting in capital letters.

## Summary

- Test prompts on many inputs; change one thing at a time.
- Automatic checks catch length, format and banned phrases.
- Ground answers in sources and allow "I don't know".

```exercise
{
  "title": "A length check",
  "prompt_md": "Complete `too_long(answer, limit)` so it returns `True` when the answer has **more words** than `limit`. The program must print exactly:\n```\nFalse\nTrue\n```",
  "starter_code": "def too_long(answer, limit):\n    pass\n\nprint(too_long(\"Thanks, it ships today.\", 10))\nprint(too_long(\"one two three four five six\", 5))",
  "solution_code": "def too_long(answer, limit):\n    return len(answer.split()) > limit\n\nprint(too_long(\"Thanks, it ships today.\", 10))\nprint(too_long(\"one two three four five six\", 5))",
  "check_type": "output",
  "expected_value": "False\nTrue",
  "hint": "return len(answer.split()) > limit"
}
```

```quiz
[
  {"question": "How should you change a prompt while testing it?", "options": ["One thing at a time, then rerun the tests", "Rewrite everything each time", "Add more capital letters"], "answer": 0, "explanation": "Then you know which change helped."},
  {"question": "Which instruction reduces made-up answers?", "options": ["Answer only from the documents; say if you don't know", "Always give an answer", "Be creative"], "answer": 0, "explanation": "Grounding plus permission to say 'I don't know'."}
]
```
