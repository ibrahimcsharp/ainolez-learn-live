from modules.assistant import knowledge
from modules.assistant.models import KBSource
from shared.jobs import job


@job("assistant.index_lesson")
def index_lesson(payload: dict) -> None:
    knowledge.index_lesson(payload["lesson_id"])


@job("assistant.index_source")
def index_source(payload: dict) -> None:
    source = KBSource.all_objects.filter(pk=payload["source_id"]).first()
    if source is None:
        return
    if source.type == KBSource.Type.LESSON:
        knowledge.index_lesson(source.lesson_id)
    else:
        knowledge.index_document(source)


@job("assistant.index_everything")
def index_everything(payload: dict) -> None:
    knowledge.index_everything()
