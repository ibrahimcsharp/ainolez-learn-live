import io
import zipfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from modules.content_tools import services
from modules.content_tools.embeds import parse_video
from shared.exceptions import ServiceError

LESSON = """---
minutes: 8
---
# Python Lists

A list holds many values.

```python tryit
fruits = ["apple", "banana"]
print(fruits)
```

{{youtube:dQw4w9WgXcQ}}

!!! note
    Lists start at index 0.
"""


def test_render_removes_scripts_and_keeps_formatting():
    html = services.render_markdown("**bold** <script>alert(1)</script> <a onclick='x()'>a</a>")
    assert "<strong>bold</strong>" in html
    assert "<script" not in html and "onclick" not in html


def test_render_expands_video_shortcode_but_not_inside_code():
    html = services.render_markdown("{{youtube:dQw4w9WgXcQ}}\n\n```\n{{youtube:dQw4w9WgXcQ}}\n```")
    assert html.count("youtube-nocookie.com/embed/dQw4w9WgXcQ") == 1
    assert "{{youtube:dQw4w9WgXcQ}}" in html


def test_iframes_from_unknown_sites_lose_their_src():
    html = services.render_markdown('<iframe src="https://evil.example.com/x"></iframe>')
    assert "evil.example.com" not in html


def test_admonition_becomes_callout_markup():
    assert 'class="admonition note"' in services.render_markdown("!!! note\n    Careful.")


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", ("youtube", "dQw4w9WgXcQ")),
        ("https://youtu.be/dQw4w9WgXcQ", ("youtube", "dQw4w9WgXcQ")),
        ("https://vimeo.com/76979871", ("vimeo", "76979871")),
        ("https://cdn.example.com/intro.mp4", ("file", "https://cdn.example.com/intro.mp4")),
        ("https://example.com/page", None),
    ],
)
def test_parse_video(url, expected):
    assert parse_video(url) == expected


def test_import_splits_lesson_into_blocks():
    [draft] = services.import_markdown_files([SimpleUploadedFile("01-lists.md", LESSON.encode())])
    assert draft.title == "Python Lists"
    assert draft.minutes == 8
    assert [block.type for block in draft.blocks] == ["markdown", "example", "video", "markdown"]
    assert draft.blocks[1].data == {
        "language": "python",
        "code": 'fruits = ["apple", "banana"]\nprint(fruits)',
    }
    assert "# Python Lists" not in draft.blocks[0].content_md  # the title is not repeated


def test_import_zip_orders_lessons_by_file_name():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("chapter/02-second.md", "# Second")
        archive.writestr("chapter/01-first.md", "# First")
        archive.writestr("chapter/notes.txt", "ignored")
    upload = SimpleUploadedFile("chapter.zip", buffer.getvalue())
    assert [d.title for d in services.import_markdown_files([upload])] == ["First", "Second"]


def test_import_rejects_other_file_types():
    with pytest.raises(ServiceError):
        services.import_markdown_files([SimpleUploadedFile("evil.exe", b"MZ")])


def test_embed_block_refuses_unknown_sites():
    with pytest.raises(ServiceError):
        services.embed_block_html({"url": "https://evil.example.com/"})
