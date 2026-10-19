"""
Checks the starter courses in database/seed/courses/ without a database:
every lesson file parses, quizzes have a valid answer, and every exercise's
solution passes its own check: Python runs with exec, SQL with sqlite3 and
JavaScript with Node.js (skipped when Node is not installed).
"""

import contextlib
import io
import json
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path

import pytest

from modules.catalog.services import EXERCISE_LANGUAGE
from modules.content_tools import services as content

SEED = Path(__file__).resolve().parents[4] / "database" / "seed" / "courses"
COURSES = sorted(p for p in SEED.iterdir() if (p / "course.json").exists())


def _lessons():
    for folder in COURSES:
        meta = json.loads((folder / "course.json").read_text(encoding="utf-8"))
        for chapter in meta["chapters"]:
            for name in chapter["lessons"]:
                language = EXERCISE_LANGUAGE.get(meta["language_key"], meta["language_key"])
                yield pytest.param(folder, name, language, id=f"{folder.name}/{name}")


def lines(text: str) -> list[str]:
    """Same comparison as assessment.services.check_exercise."""
    return [line.rstrip() for line in (text or "").strip().splitlines()]


def run_python(code: str) -> str:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code, "<solution>", "exec"), {"__name__": "__main__"})  # our own content
    return output.getvalue()


def run_sql(code: str) -> str:
    """Formats results like the browser's sql.js runner: header and rows, tab separated."""
    db = sqlite3.connect(":memory:")
    results, statement = [], ""
    for line in code.splitlines(keepends=True):
        statement += line
        if sqlite3.complete_statement(statement):
            cursor = db.execute(statement)
            if cursor.description:
                header = "\t".join(column[0] for column in cursor.description)
                rows = ["\t".join(str(v) for v in row) for row in cursor.fetchall()]
                results.append("\n".join([header, *rows]))
            statement = ""
    return "\n\n".join(results)


def run_javascript(code: str) -> str:
    node = shutil.which("node")
    if not node:
        pytest.skip("Node.js is not installed here (the browser runs JavaScript)")
    done = subprocess.run([node, "-e", code], capture_output=True, text=True, timeout=10)
    assert done.returncode == 0, done.stderr
    return done.stdout


RUNNERS = {"python": run_python, "sql": run_sql, "javascript": run_javascript}


def test_course_files_are_complete():
    assert len(COURSES) >= 10
    for folder in COURSES:
        meta = json.loads((folder / "course.json").read_text(encoding="utf-8"))
        listed = {name for chapter in meta["chapters"] for name in chapter["lessons"]}
        assert listed == {p.name for p in folder.glob("*.md")}, folder.name


@pytest.mark.parametrize(("folder", "name", "language"), list(_lessons()))
def test_lesson(folder, name, language, tmp_path, monkeypatch):
    draft = content.parse_lesson_markdown((folder / name).read_text(encoding="utf-8"), name)
    assert draft.summary and draft.slug, "front matter needs summary and slug"
    for block in draft.blocks:
        if block.type == "quiz":
            for question in block.data["questions"]:
                assert 0 <= question["answer"] < len(question["options"]), question["question"]
        if block.type == "exercise":
            check_exercise(block.data, language, tmp_path, monkeypatch)


def check_exercise(exercise, language, tmp_path, monkeypatch):
    solution, expected = exercise["solution_code"], exercise["expected_value"]
    kind = exercise["check_type"]
    if kind == "contains":
        assert expected in solution, exercise["title"]
    elif kind == "regex":
        assert re.search(expected, solution, re.MULTILINE), exercise["title"]
    elif kind == "exact":
        assert lines(solution) == lines(expected), exercise["title"]
    else:
        monkeypatch.chdir(tmp_path)  # exercises may write files
        run = RUNNERS[exercise.get("language", language)]
        try:
            printed = run(solution)
        except ImportError as exc:
            pytest.skip(f"{exc.name} is not installed here (it is in the browser)")
        assert lines(printed) == lines(expected), exercise["title"]
