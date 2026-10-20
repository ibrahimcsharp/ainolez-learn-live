"""
In-process domain events, so modules can react to each other without imports.

    # modules/learning/events.py
    @dataclass(frozen=True)
    class CourseCompleted:
        user_id: int
        course_id: int

    # modules/certification/handlers.py
    @subscribe(CourseCompleted)
    def issue_certificate(event): ...

    publish(CourseCompleted(user_id=7, course_id=3))

Handlers run straight away, inside the publisher's transaction, so either
everything is saved or nothing is. Slow work in a handler belongs in a job.
"""

from collections import defaultdict
from collections.abc import Callable

_subscribers: dict[type, list[Callable]] = defaultdict(list)


def subscribe(event_type: type):
    def register(handler: Callable):
        _subscribers[event_type].append(handler)
        return handler

    return register


def publish(event) -> None:
    for handler in _subscribers[type(event)]:
        handler(event)
