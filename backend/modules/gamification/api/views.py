from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.gamification import selectors


class LeaderboardView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        period = request.query_params.get("period", "week")
        if period not in selectors.PERIODS:
            period = "week"
        return Response({"period": period, "leaders": selectors.leaderboard(period)})
