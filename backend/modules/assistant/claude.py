"""
The only place that talks to the Claude API (official `anthropic` SDK).

Streaming is used on the server side so long answers do not time out; the
browser still gets one JSON reply, because cPanel's Passenger may buffer
streamed responses. `fallbacks="default"` lets the API retry a declined
request on a suitable model instead of refusing outright.
"""

import logging
import time
from dataclasses import dataclass

import anthropic
from django.conf import settings

from shared.exceptions import ServiceError

logger = logging.getLogger(__name__)

FALLBACK_BETA = "server-side-fallback-2026-07-01"
# US dollars per million tokens (input, output), for the cost estimate on the usage page.
PRICES = {
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
}
MODELS = tuple(PRICES)


@dataclass
class ModelReply:
    text: str
    model: str
    tokens_in: int  # all input tokens, cached or not
    tokens_out: int
    cached_tokens: int
    cost: float
    latency_ms: int
    refused: bool
    cut_short: bool  # hit max_tokens


def complete(
    *,
    model: str,
    effort: str,
    max_tokens: int,
    system: str,
    messages: list[dict],
    json_schema: dict | None = None,
    thinking: bool = False,
) -> ModelReply:
    """One Claude call. With `json_schema` the reply text is JSON matching it
    (structured outputs); `thinking` turns on adaptive thinking for harder work."""
    if not settings.ANTHROPIC_API_KEY:
        raise ServiceError("The AI tutor is not set up yet.", "ai_not_configured", 503)
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY, timeout=90.0, max_retries=2)
    output_config = {"effort": effort}
    if json_schema:
        output_config["format"] = {"type": "json_schema", "schema": json_schema}
    extra = {"thinking": {"type": "adaptive"}} if thinking else {}
    started = time.monotonic()
    try:
        with client.beta.messages.stream(
            model=model,
            max_tokens=max_tokens,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            output_config=output_config,
            # Instructions never change between requests, so they are cached.
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=messages,
            **extra,
        ) as stream:
            message = stream.get_final_message()
    except (
        anthropic.RateLimitError,
        anthropic.APIConnectionError,
        anthropic.InternalServerError,
    ) as exc:
        logger.warning("Claude API busy: %s", exc)
        raise ServiceError(
            "The AI tutor is busy right now. Please try again in a minute.", "ai_busy", 503
        ) from exc
    except anthropic.APIStatusError as exc:
        logger.error(
            "Claude API error %s (request %s): %s", exc.status_code, exc.request_id, exc.message
        )
        raise ServiceError("The AI tutor could not answer this time.", "ai_error", 502) from exc

    usage = message.usage
    written = usage.cache_creation_input_tokens or 0
    read = usage.cache_read_input_tokens or 0
    price_in, price_out = PRICES.get(message.model, PRICES["claude-opus-5-5"])
    cost = (
        price_in * (usage.input_tokens + 1.25 * written + 0.1 * read)
        + price_out * usage.output_tokens
    ) / 1e6
    return ModelReply(
        text="".join(block.text for block in message.content if block.type == "text").strip(),
        model=message.model,
        tokens_in=usage.input_tokens + written + read,
        tokens_out=usage.output_tokens,
        cached_tokens=read,
        cost=cost,
        latency_ms=int((time.monotonic() - started) * 1000),
        refused=message.stop_reason == "refusal",
        cut_short=message.stop_reason == "max_tokens",
    )
