"""Instructions and JSON schemas for the course generator's two Claude calls."""

SYSTEM = """You write free courses for ainolez, a W3Schools-style learning website
("Learn it. Code it. Own it."). Learners read short lessons, run examples in the
browser and check themselves with exercises and quizzes.

Style:
- Plain, friendly English for an international audience. Short sentences and paragraphs.
- Teach one idea at a time: explain it, show a small runnable example, then explain the output.
- Match the level you are given. Beginners get no unexplained jargon.
- Be accurate. Use current, standard syntax and libraries. Never invent APIs.
- No marketing language, no emoji, no links to other websites."""

OUTLINE_TASK = """Plan a course.

Topic: {topic}
Level: {level}
Audience: {audience}
Main language of the code: {language}
Chapters: exactly {chapters}
Lessons per chapter: about {lessons}
Notes from the editor: {notes}

Order the chapters from first steps to a small final project. Lesson titles are
short (2 to 6 words) and specific, like a W3Schools page title ("Python Lists",
"List Comprehension"). Each summary is one sentence saying what the learner can do
after the lesson."""

LESSON_TASK = """Write one lesson of the course "{course}" ({level}, for {audience}).

Course outline (for context, write only the lesson marked >>):
{outline}

Lesson: {title}
What the learner should be able to do after it: {summary}

Rules for "markdown":
- GitHub Markdown. Do not start with a "# " heading (the page shows the title).
  Use "## " for sections.
- 300 to 700 words.
- Put every example the learner should run in a fence marked tryit, e.g.
  ```{fence} tryit
  ...
  ```
  {runner}
- Plain code that should not get a Run button uses a normal fence.
- End with a short "## Summary" of 2 to 4 bullet points.

Rules for "exercise": one small task in {exercise_language} that practises this lesson.
Prefer check_type "output": expected_value is exactly what the solution prints
(Python and SQL) or a short piece of code the answer must contain (HTML, CSS, JavaScript,
then use "contains"). starter_code is a starting point, not the solution. The hint
nudges without giving the answer away.

Rules for "quiz": 3 multiple-choice questions about this lesson, each with 3 or 4
options and exactly one correct option (correct_index starts at 0). The explanation
says why the answer is right."""

RUNNERS = {
    "python": (
        "Python runs in the browser with Pyodide: no input(), no files, no network. "
        "numpy, pandas, matplotlib and scikit-learn can be imported."
    ),
    "sql": (
        "SQL runs in SQLite in the browser. "
        "Each example must create and fill the tables it queries."
    ),
    "html": "HTML examples are full small pages; CSS and JavaScript go inside them.",
    "css": "Write a full small HTML page with the CSS in a <style> tag, fence it as html.",
    "javascript": "JavaScript runs in a page; use console.log or change the page to show results.",
}

OUTLINE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "short_description": {"type": "string"},
        "description": {"type": "string"},
        "chapters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "lessons": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "summary": {"type": "string"},
                            },
                            "required": ["title", "summary"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["title", "description", "lessons"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "short_description", "description", "chapters"],
    "additionalProperties": False,
}

LESSON_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "minutes": {"type": "integer"},
        "markdown": {"type": "string"},
        "exercise": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "prompt_md": {"type": "string"},
                "starter_code": {"type": "string"},
                "solution_code": {"type": "string"},
                "check_type": {"type": "string", "enum": ["output", "contains", "exact", "regex"]},
                "expected_value": {"type": "string"},
                "hint": {"type": "string"},
            },
            "required": [
                "title",
                "prompt_md",
                "starter_code",
                "solution_code",
                "check_type",
                "expected_value",
                "hint",
            ],  # fmt: skip
            "additionalProperties": False,
        },
        "quiz": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "correct_index": {"type": "integer"},
                    "explanation": {"type": "string"},
                },
                "required": ["question", "options", "correct_index", "explanation"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["summary", "minutes", "markdown", "exercise", "quiz"],
    "additionalProperties": False,
}
