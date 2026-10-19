# Starter courses

`manage.py seed_courses` loads every folder in `courses/` as a published course
(existing slugs are skipped). One folder per course:

- `course.json`: title, slug, category, level, language, descriptions, and the
  chapters with their lesson files in order.
- `*.md`: one lesson each, in the same format as the admin's Markdown import:
  - front matter `title`, `summary`, `minutes`
  - ```` ```python tryit ```` fences become "Try it Yourself" examples
  - ```` ```exercise ```` holds an exercise as JSON
  - ```` ```quiz ```` holds quiz questions as JSON (`answer` is the index of the right option)

`python manage.py seed_courses python sql` loads only those folders; `--draft` loads them unpublished.
