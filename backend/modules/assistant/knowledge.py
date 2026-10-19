"""
The tutor's knowledge base: our lessons and admin documents, split into
chunks (kb_chunks) and found again with MySQL FULLTEXT search.
"""

import hashlib
import re
from dataclasses import dataclass

from django.db import connection, transaction
from django.utils import timezone

from modules.assistant.models import KBChunk, KBSource
from modules.catalog import selectors as catalog

CHUNK_CHARS = 3000  # about 800 tokens
CANDIDATES = 30


@dataclass
class Excerpt:
    title: str
    url: str
    text: str
    score: float


def index_lesson(lesson_id: int) -> None:
    """Bring one lesson's chunks up to date, or retire them if the lesson is now hidden."""
    lesson = catalog.lesson_for_index(lesson_id)
    source = KBSource.all_objects.filter(type=KBSource.Type.LESSON, lesson_id=lesson_id).first()
    if lesson is None:
        if source:
            source.delete()  # chunks go with it
        return
    source = source or KBSource(type=KBSource.Type.LESSON, lesson_id=lesson_id)
    source.title, source.url = lesson["title"], lesson["url"]
    _index(source, lesson["text"], lesson_id=lesson_id, course_id=lesson["course_id"])


def index_document(source: KBSource) -> None:
    _index(source, source.body or "")


def index_everything() -> dict[str, int]:
    """Nightly: index every visible lesson and document, and drop lessons that went away."""
    visible = catalog.all_visible_lesson_ids()
    stale = KBSource.all_objects.filter(type=KBSource.Type.LESSON).exclude(lesson_id__in=visible)
    removed = stale.count()
    stale.delete()
    for lesson_id in visible:
        index_lesson(lesson_id)
    documents = KBSource.objects.filter(type=KBSource.Type.DOCUMENT)
    for document in documents:
        index_document(document)
    return {"lessons": len(visible), "documents": documents.count(), "removed": removed}


def search(
    question: str, lesson_id: int | None = None, course_id: int | None = None, limit: int = 4
):
    """Best excerpts for a question. Chunks of the open lesson rank higher, then its course."""
    excerpts: list[Excerpt] = []
    if lesson_id:  # "explain this lesson" shares no words with it, so always include its start
        own = KBChunk.objects.filter(lesson_id=lesson_id, source__is_active=True).select_related(
            "source"
        )
        for chunk in own.order_by("chunk_no")[:2]:
            excerpts.append(Excerpt(chunk.source.title, chunk.source.url, chunk.text, score=1e9))
    for row in _fulltext(question):
        chunk_id, text, chunk_lesson, chunk_course, title, url, score = row
        if chunk_lesson == lesson_id and lesson_id:
            continue  # already included above
        boost = 1.3 if course_id and chunk_course == course_id else 1.0
        excerpts.append(Excerpt(title, url, text, score * boost))
    excerpts.sort(key=lambda e: e.score, reverse=True)
    return excerpts[:limit]


def _index(source: KBSource, text: str, lesson_id: int | None = None, course_id: int | None = None):
    digest = hashlib.sha256(f"{source.title}\n{text}".encode()).hexdigest()
    if source.pk and source.content_hash == digest and source.status == KBSource.Status.INDEXED:
        return  # nothing changed
    chunks = split_text(text, header=source.title)
    with transaction.atomic():
        source.content_hash = digest
        source.chunk_count = len(chunks)
        source.status = KBSource.Status.INDEXED
        source.error = ""
        source.last_indexed_at = timezone.now()
        source.save()
        source.chunks.all().delete()
        KBChunk.objects.bulk_create(
            KBChunk(source=source, chunk_no=i, text=chunk, lesson_id=lesson_id, course_id=course_id)
            for i, chunk in enumerate(chunks)
        )


def split_text(text: str, header: str = "") -> list[str]:
    """Paragraph-aligned chunks of about CHUNK_CHARS, each starting with the source title."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, current = [], ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) > CHUNK_CHARS:
            chunks.append(current)
            current = ""
        current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return [f"{header}\n\n{chunk}" if header else chunk for chunk in chunks]


def _fulltext(question: str) -> list[tuple]:
    words = " ".join(re.findall(r"\w+", question))[:500]
    if not words:
        return []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.id, c.text, c.lesson_id, c.course_id, s.title, s.url,
                   MATCH(c.text) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
            FROM kb_chunks c
            JOIN kb_sources s ON s.id = c.source_id
            WHERE s.is_active = 1 AND s.deleted_at IS NULL
              AND MATCH(c.text) AGAINST (%s IN NATURAL LANGUAGE MODE)
            ORDER BY score DESC
            LIMIT %s
            """,
            [words, words, CANDIDATES],
        )
        rows = cursor.fetchall()
    # A lesson may have been hidden since it was indexed: never quote hidden content.
    visible = catalog.lesson_links(r[2] for r in rows if r[2])
    return [r for r in rows if r[2] is None or r[2] in visible]
