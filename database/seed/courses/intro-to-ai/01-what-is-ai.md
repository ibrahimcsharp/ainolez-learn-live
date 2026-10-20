---
title: What Is Artificial Intelligence?
slug: what-is-ai
summary: Understand what AI means, the difference between rules and learning, and where AI is used today.
minutes: 7
---
## A working definition

**Artificial intelligence (AI)** is the field of building computer systems that do tasks we normally think need human intelligence: understanding language, recognising images, making predictions, planning and deciding.

AI is not one technology. It is a family of methods, and today most of them are **machine learning**: systems that learn patterns from examples instead of following rules a person wrote.

## Rules versus learning

Imagine sorting emails into spam and not spam.

**The rules approach**: a programmer writes the rules.

```python tryit
def is_spam(email):
    words = ["winner", "free money", "click now"]
    return any(word in email.lower() for word in words)

print(is_spam("You are a WINNER! Click now"))
print(is_spam("Lunch at noon?"))
```

This works until spammers change their words. Someone must keep writing new rules.

**The learning approach**: give the computer thousands of emails already labelled "spam" or "not spam" and let it find the patterns itself. When spam changes, you retrain it on new examples. You will see how in the next lesson.

## AI you already use

- Recommendations on video and shopping sites.
- Maps that predict traffic.
- Photo apps that find faces.
- Translation, speech-to-text and voice assistants.
- Chat assistants such as Claude, which write, summarise and answer questions.

## Narrow AI and general AI

Every AI system today is **narrow**: very good at specific kinds of tasks. **Artificial general intelligence** (AGI), a system as broadly capable as a person at almost everything, is a research goal and a topic of debate, not something you can assume a tool has.

## Terms you will hear

| Term | Meaning |
|------|---------|
| AI | the whole field |
| Machine learning (ML) | learning patterns from data |
| Deep learning | ML with large neural networks |
| Generative AI | models that create text, images, audio or code |
| Model | the trained result you use to make predictions |

## Summary

- AI = systems doing tasks that need intelligence.
- Most modern AI is machine learning: learning from examples, not hand-written rules.
- Today's AI is narrow: strong at specific tasks.

```exercise
{
  "title": "Your own rule",
  "prompt_md": "Complete `is_question` so it returns `True` when the text ends with `?`. The program must print exactly:\n```\nTrue\nFalse\n```",
  "starter_code": "def is_question(text):\n    pass\n\nprint(is_question(\"Is it raining?\"))\nprint(is_question(\"It is raining.\"))",
  "solution_code": "def is_question(text):\n    return text.strip().endswith(\"?\")\n\nprint(is_question(\"Is it raining?\"))\nprint(is_question(\"It is raining.\"))",
  "check_type": "output",
  "expected_value": "True\nFalse",
  "hint": "return text.strip().endswith(\"?\")"
}
```

```quiz
[
  {"question": "What is machine learning?", "options": ["Systems that learn patterns from examples", "Robots building machines", "Programs that follow only hand-written rules"], "answer": 0, "explanation": "ML finds patterns in data instead of using only fixed rules."},
  {"question": "What kind of AI exists today?", "options": ["Narrow AI, strong at specific tasks", "General AI equal to humans at everything", "Conscious AI"], "answer": 0, "explanation": "Current systems are narrow, however impressive."}
]
```
