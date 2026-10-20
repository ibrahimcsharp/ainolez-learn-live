from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from modules.identity import services
from modules.identity.api import serializers as s
from shared.audit import client_ip


class PublicAuthView(APIView):
    """Open to visitors, rate limited."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def validated(self, serializer_class):
        serializer = serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


def _message(text: str, code=status.HTTP_200_OK) -> Response:
    return Response({"detail": text}, status=code)


def _set_refresh_cookie(response: Response, refresh) -> None:
    cookie = settings.REFRESH_COOKIE
    response.set_cookie(
        cookie["key"],
        str(refresh),
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path=cookie["path"],
        httponly=cookie["httponly"],
        secure=cookie["secure"],
        samesite=cookie["samesite"],
    )


class RegisterView(PublicAuthView):
    def post(self, request):
        services.register_learner(**self.validated(s.RegisterSerializer))
        return _message("Account created. Check your email to verify it.", status.HTTP_201_CREATED)


class VerifyEmailView(PublicAuthView):
    def post(self, request):
        services.verify_email(self.validated(s.TokenSerializer)["token"])
        return _message("Email verified. You can log in now.")


class ResendVerificationView(PublicAuthView):
    def post(self, request):
        services.resend_verification(self.validated(s.EmailSerializer)["email"])
        return _message("If that account needs verifying, a new email is on its way.")


class LoginView(PublicAuthView):
    def post(self, request):
        user, refresh = services.login(**self.validated(s.LoginSerializer), ip=client_ip(request))
        response = Response(
            {"access": str(refresh.access_token), "user": s.UserSerializer(user).data}
        )
        _set_refresh_cookie(response, refresh)
        return response


class RefreshView(PublicAuthView):
    """Swaps the refresh cookie for a new access token (and a rotated cookie)."""

    def post(self, request):
        raw = request.COOKIES.get(settings.REFRESH_COOKIE["key"])
        if not raw:
            return _message("Not logged in.", status.HTTP_401_UNAUTHORIZED)
        serializer = TokenRefreshSerializer(data={"refresh": raw})
        try:
            serializer.is_valid(raise_exception=True)
        # expired, revoked or tampered cookie, or its user was deleted or disabled
        except (TokenError, ObjectDoesNotExist, AuthenticationFailed):
            response = _message(
                "Session expired. Please log in again.", status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie(
                settings.REFRESH_COOKIE["key"], path=settings.REFRESH_COOKIE["path"]
            )
            return response
        response = Response({"access": serializer.validated_data["access"]})
        _set_refresh_cookie(response, serializer.validated_data["refresh"])
        return response


class LogoutView(PublicAuthView):
    def post(self, request):
        raw = request.COOKIES.get(settings.REFRESH_COOKIE["key"])
        if raw:
            try:
                RefreshToken(raw).blacklist()
            except TokenError:
                pass  # already expired or revoked
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.REFRESH_COOKIE["key"], path=settings.REFRESH_COOKIE["path"])
        return response


class ForgotPasswordView(PublicAuthView):
    def post(self, request):
        services.request_password_reset(self.validated(s.EmailSerializer)["email"])
        return _message("If an account exists for that email, a reset link is on its way.")


class ResetPasswordView(PublicAuthView):
    def post(self, request):
        data = self.validated(s.ResetPasswordSerializer)
        services.reset_password(data["token"], data["password"])
        return _message("Password changed. Please log in.")


class MeView(APIView):
    def get(self, request):
        return Response(s.UserSerializer(request.user).data)

    def patch(self, request):
        serializer = s.ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.update_profile(request.user, **serializer.validated_data)
        return Response(s.UserSerializer(user).data)
