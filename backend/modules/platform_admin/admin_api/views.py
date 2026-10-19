from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView

from modules.catalog import selectors as catalog
from modules.certification import selectors as certification
from modules.community import selectors as community
from modules.identity import selectors as identity
from modules.learning import selectors as learning
from modules.seo import selectors as seo
from shared.permissions import IsSuperAdmin
from shared.stats import first_day


class DashboardView(APIView):
    """Numbers for the admin dashboard. More cards arrive with each sprint."""

    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response({
            "users": identity.user_counts(),
            "catalog": catalog.catalog_counts(),
            "certificates": certification.counts(),
            "community": community.counts(),
        })  # fmt: skip


class AnalyticsView(APIView):
    """Daily activity for the last 7, 30 or 90 days: visits, signups and learning."""

    permission_classes = [IsSuperAdmin]
    PERIODS = ("7", "30", "90")

    def get(self, request):
        days = request.query_params.get("days")
        days = int(days) if days in self.PERIODS else 30
        series = {
            "page_views": seo.views_by_day(days),
            "signups": identity.signups_by_day(days),
            **learning.activity_by_day(days),
        }
        first = first_day(days)
        dates = [(first + timedelta(days=n)).isoformat() for n in range(days)]
        courses = learning.top_courses(days)
        titles = catalog.course_summaries(row["course_id"] for row in courses)
        return Response({
            "days": dates,
            "series": {name: [values.get(d, 0) for d in dates] for name, values in series.items()},
            "totals": {name: sum(values.values()) for name, values in series.items()},
            "top_pages": seo.top_pages(days, limit=10),
            "top_courses": [
                {**row, "title": titles.get(row["course_id"], {}).get("title", "(deleted course)")}
                for row in courses
            ],
        })  # fmt: skip
