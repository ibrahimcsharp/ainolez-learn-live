---
title: Examples and Structure
slug: examples-structure
summary: Show the model examples of what you want and separate instructions from data with tags.
minutes: 7
---
## Show, don't only tell

Examples are one of the strongest tools you have. Two or three good examples ("few-shot" prompting) show style, length and format better than a paragraph of rules.

```
Turn each customer note into a short, polite reply.

Note: "Parcel arrived broken!!"
Reply: "I'm sorry your parcel arrived damaged. I've sent a replacement today, at no cost."

Note: "Wrong size sent"
Reply: "Sorry about the mix-up. A free return label is in your email; the right size ships as soon as we scan it."

Note: "Never got my refund"
Reply:
```

Make examples varied (different situations) so the model learns the pattern, not one example's details.

## Separate instructions from data

When a prompt mixes instructions with a long document, the model can confuse the two. Wrap each part in clear tags:

```
Summarise the report for the board in five bullet points.
Use only facts from the report.

<report>
...the full report text...
</report>
```

Tags such as `<report>`, `<email>` or `<example>` have no special meaning; they just make boundaries obvious. Put long documents **first** and your question **after** them.

## A prompt template in code

```python tryit
examples = [
    ("Parcel arrived broken!!", "I'm sorry your parcel arrived damaged. A replacement ships today."),
    ("Wrong size sent", "Sorry about the mix-up. A free return label is in your email."),
]

def build_prompt(note):
    shots = "\n".join(
        f"<example>\nNote: {n}\nReply: {r}\n</example>" for n, r in examples
    )
    return f"Turn the customer note into a short, polite reply.\n\n{shots}\n\nNote: {note}\nReply:"

print(build_prompt("Never got my refund"))
```

## Summary

- Two or three varied examples teach format and style fast.
- Wrap documents and examples in tags to separate them from instructions.
- Long material first, the question last.

```exercise
{
  "title": "Wrap the document",
  "prompt_md": "Complete `wrap(text)` so it returns the text inside `<document>` tags on their own lines. The program must print exactly:\n```\n<document>\nSales rose 12%.\n</document>\n```",
  "starter_code": "def wrap(text):\n    pass\n\nprint(wrap(\"Sales rose 12%.\"))",
  "solution_code": "def wrap(text):\n    return f\"<document>\\n{text}\\n</document>\"\n\nprint(wrap(\"Sales rose 12%.\"))",
  "check_type": "output",
  "expected_value": "<document>\nSales rose 12%.\n</document>",
  "hint": "return f\"<document>\\n{text}\\n</document>\""
}
```

```quiz
[
  {"question": "What is few-shot prompting?", "options": ["Including a few examples of the desired output", "Asking very short questions", "Sending a prompt several times"], "answer": 0, "explanation": "Examples show the pattern you want."},
  {"question": "Why wrap a document in tags like <report>?", "options": ["To separate data from instructions clearly", "Tags are required by every model", "To make the prompt shorter"], "answer": 0, "explanation": "Clear boundaries prevent confusion."}
]
```
