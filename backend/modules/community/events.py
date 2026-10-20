from dataclasses import dataclass


@dataclass(frozen=True)
class PostApproved:
    user_id: int
    post_id: int


@dataclass(frozen=True)
class ReplyMarkedHelpful:
    """The post's author accepted someone else's reply as the answer."""

    user_id: int  # who wrote the reply
    reply_id: int
