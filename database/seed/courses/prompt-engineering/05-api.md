---
title: Calling Claude from Python
slug: claude-api
summary: Send prompts from your own program with the Anthropic Python SDK, and keep your API key safe.
minutes: 8
---
## From chat to code

Chat apps are great for one-off tasks. To build AI into your own app, a program sends the prompt to a model's **API** and gets the reply back. This lesson uses Claude from Anthropic; other providers work in a similar way.

## Setup (on your computer)

```
pip install anthropic
```

Create an API key in the Anthropic Console and store it in an environment variable, **never in your code**:

```
# macOS / Linux
export ANTHROPIC_API_KEY="your-key"
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your-key"
```

!!! warning
    Anyone with your key can spend your money. Do not paste it into code you share, commit it to Git or put it in a web page's JavaScript.

## Your first request

```python
import anthropic

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    system="You are a patient tutor. Explain simply.",
    messages=[{"role": "user", "content": "What is a Python list?"}],
)
print(message.content[0].text)
```

- `system` sets the role and rules for the whole conversation.
- `messages` is the conversation so far: `user` and `assistant` turns.
- `max_tokens` limits the length of the reply.

## A conversation

The API does not remember earlier calls. To continue a conversation, send the whole history each time:

```python tryit
history = [
    {"role": "user", "content": "What is a list?"},
    {"role": "assistant", "content": "A list holds several values in order."},
]
history.append({"role": "user", "content": "How do I add an item?"})

for turn in history:
    print(f"{turn['role']:>9}: {turn['content']}")
print(len(history), "messages would be sent")
```

## Costs and limits

You pay per **token**, for both the prompt and the reply. Keep prompts focused, set `max_tokens`, and cache answers to repeated questions. This site's AI tutor answers common questions from a saved FAQ before it calls the model, for exactly this reason.

## Summary

- Install the SDK, keep the key in an environment variable.
- `client.messages.create(model=..., system=..., messages=[...])` sends a prompt.
- Send the full history for conversations; watch token costs.

```exercise
{
  "title": "Build the message list",
  "prompt_md": "Append a user message with the content `Thanks!` to `history` and print the number of messages. The output must be exactly `3`",
  "starter_code": "history = [\n    {\"role\": \"user\", \"content\": \"Hi\"},\n    {\"role\": \"assistant\", \"content\": \"Hello! How can I help?\"},\n]\n",
  "solution_code": "history = [\n    {\"role\": \"user\", \"content\": \"Hi\"},\n    {\"role\": \"assistant\", \"content\": \"Hello! How can I help?\"},\n]\nhistory.append({\"role\": \"user\", \"content\": \"Thanks!\"})\nprint(len(history))",
  "check_type": "output",
  "expected_value": "3",
  "hint": "history.append({\"role\": \"user\", \"content\": \"Thanks!\"})"
}
```

```quiz
{
  "title": "Final quiz: Prompt Engineering",
  "final": true,
  "questions": [
    {"question": "What improves a vague prompt the most?", "options": ["Adding context: audience, goal, format", "Making it shorter", "Adding exclamation marks"], "answer": 0, "explanation": "The model needs to know your situation."},
    {"question": "Why include examples in a prompt?", "options": ["They show the format and style you want", "They make the model faster", "They are required"], "answer": 0, "explanation": "Few-shot examples teach the pattern."},
    {"question": "What should a program do with a model's JSON reply?", "options": ["Parse and validate it", "Trust it fully", "Print it only"], "answer": 0, "explanation": "Always check model output."},
    {"question": "How do you test a prompt properly?", "options": ["Run it on many test cases and change one thing at a time", "Try it once", "Ask the model if the prompt is good"], "answer": 0, "explanation": "Prompts are code; test them."},
    {"question": "Where should an API key live?", "options": ["In an environment variable, out of shared code", "In the web page's JavaScript", "In a public Git repository"], "answer": 0, "explanation": "Anyone with the key can use your account."},
    {"question": "Does the API remember earlier calls?", "options": ["No, you send the history each time", "Yes, forever", "Only on Sundays"], "answer": 0, "explanation": "Each request must contain the conversation so far."}
  ]
}
```
