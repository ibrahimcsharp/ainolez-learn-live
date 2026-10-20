"""
Applies the hand-written SQL files in database/schema/ in name order, once each.

Applied files are recorded in the ``schema_migrations`` table. Never edit a
file that has been applied anywhere; add a new numbered file instead.
Statements are split on ";" so do not put semicolons inside SQL strings.
"""

from pathlib import Path

from django.conf import settings
from django.db import connections

TRACKING_TABLE = """
CREATE TABLE IF NOT EXISTS schema_migrations (
  filename   VARCHAR(255) NOT NULL,
  applied_at DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (filename)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""


def apply_pending(using: str = "default") -> list[str]:
    """Run every SQL file not yet applied. Returns the names of files applied now."""
    applied_now = []
    with connections[using].cursor() as cursor:
        cursor.execute(TRACKING_TABLE)
        cursor.execute("SELECT filename FROM schema_migrations")
        already_applied = {row[0] for row in cursor.fetchall()}

        for path in sorted(Path(settings.SCHEMA_DIR).glob("*.sql")):
            if path.name in already_applied:
                continue
            for statement in split_statements(path.read_text(encoding="utf-8")):
                cursor.execute(statement)
            cursor.execute("INSERT INTO schema_migrations (filename) VALUES (%s)", [path.name])
            applied_now.append(path.name)
    return applied_now


def split_statements(sql: str) -> list[str]:
    lines = [line for line in sql.splitlines() if not line.lstrip().startswith("--")]
    return [part.strip() for part in "\n".join(lines).split(";") if part.strip()]
