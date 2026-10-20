---
title: Output Formats and Big Tasks
slug: output-formats
summary: Ask for exact formats such as JSON, and split big tasks into steps.
minutes: 8
---
## Ask for the format you need

If a person reads the answer, describe the layout: "three short paragraphs", "a table with columns Name and Reason". If a **program** reads the answer, ask for a strict format such as JSON and describe its fields:

```
Extract the event from the email. Reply with only a JSON object with the keys
"title" (string), "date" (YYYY-MM-DD) and "attendees" (list of names).

<email>
Hi all, the design review is on 14 March 2026. Amara, Ben and Chen please join.
</email>
```

Many AI services can also **enforce** a JSON schema, so the reply always parses. This site's AI course generator does exactly that.

## Check what comes back

Never trust model output blindly in a program. Parse it and validate it:

```python tryit
import json

reply = '{"title": "Design review", "date": "2026-03-14", "attendees": ["Amara", "Ben", "Chen"]}'

event = json.loads(reply)
assert set(event) == {"title", "date", "attendees"}, "unexpected keys"
assert isinstance(event["attendees"], list)
print(event["title"], "on", event["date"], "with", len(event["attendees"]), "people")
```

## Break big tasks into steps

One giant prompt ("research, outline, write and edit a report") gives average results. A chain of focused prompts does better, and each step can be checked:

1. Extract the key facts from the sources.
2. Make an outline from the facts.
3. Write each section from the outline.
4. Review the draft against the facts.

## Let the model think first

For problems with several steps (maths, planning, debugging), ask the model to work through the problem before giving the final answer. Modern models such as Claude can also "think" internally before they answer when that option is turned on.

## Summary

- Describe the exact format; use JSON for programs.
- Always parse and validate model output.
- Split large tasks into a chain of smaller prompts.

```exercise
{
  "title": "Validate the reply",
  "prompt_md": "Parse `reply` with `json.loads` and print the **number of attendees**. The output must be exactly `3`",
  "starter_code": "import json\n\nreply = '{\"title\": \"Kick-off\", \"attendees\": [\"Mia\", \"Leo\", \"Ava\"]}'\n",
  "solution_code": "import json\n\nreply = '{\"title\": \"Kick-off\", \"attendees\": [\"Mia\", \"Leo\", \"Ava\"]}'\nevent = json.loads(reply)\nprint(len(event[\"attendees\"]))",
  "check_type": "output",
  "expected_value": "3",
  "hint": "event = json.loads(reply); print(len(event[\"attendees\"]))"
}
```

```quiz
[
  {"question": "Your program needs the model's answer as data. What should you ask for?", "options": ["A strict format such as JSON with named fields", "A friendly paragraph", "As much detail as possible"], "answer": 0, "explanation": "Programs need a predictable, parseable format."},
  {"question": "Why split a big task into several prompts?", "options": ["Each step is focused and can be checked", "Models cannot read long prompts", "It is always cheaper"], "answer": 0, "explanation": "Chains of focused steps are more reliable."}
]
```
