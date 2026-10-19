import logging

from modules.seo import prerender, services
from shared.exceptions import ServiceError
from shared.jobs import job

logger = logging.getLogger(__name__)


@job(services.BUILD_JOB)
def build(payload: dict) -> None:
    try:
        prerender.build()
    except ServiceError as exc:
        logger.warning("SEO build skipped: %s", exc)  # e.g. PRERENDER_DIR not set on this PC
