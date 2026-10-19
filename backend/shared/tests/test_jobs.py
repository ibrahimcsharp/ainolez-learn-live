import pytest

from shared import jobs
from shared.models import Job

pytestmark = pytest.mark.django_db
payload_seen = []


@jobs.job("test.always_fails")
def _always_fails(payload):
    raise RuntimeError("boom")


@jobs.job("test.records")
def _records(payload):
    payload_seen.append(payload)


def test_job_runs_once():
    jobs.enqueue("test.records", {"n": 1})
    assert jobs.run_pending() == 1
    assert payload_seen == [{"n": 1}]
    assert Job.objects.get().status == Job.Status.DONE


def test_failed_job_is_retried_later_then_marked_failed():
    item = jobs.enqueue("test.always_fails")
    jobs.run_pending()
    item.refresh_from_db()
    assert item.status == Job.Status.QUEUED and item.attempts == 1
    assert "boom" in item.last_error

    for _ in range(jobs.MAX_ATTEMPTS - 1):
        Job.objects.filter(pk=item.pk).update(run_after=item.created_at)  # skip back-off
        jobs.run_pending()
    item.refresh_from_db()
    assert item.status == Job.Status.FAILED


def test_unknown_job_type_is_refused():
    with pytest.raises(ValueError):
        jobs.enqueue("test.missing")
