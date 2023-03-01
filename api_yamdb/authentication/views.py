from rest_framework.views import APIView
from .serializers import UserCreationSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from users.models import User
from rest_framework.response import Response
from rest_framework import status


def get_token(self, user):
    """."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': refresh,
        'access': str(refresh.access_token)
    }


class RegistrationClass(APIView):
    """."""

    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(**serializer.data)
            user.is_active = False
            confirmation_code = user.make_confirmation_code()
            send_mail(
                'welcome',
                f'{confirmation_code}',
                'EMAIL_HOST',
                [f'{user.email}', ]
            )
            user.confirmation_code = User.hash_confirmation_code(
                self, confirmation_code
            )
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedClass(APIView):
    """."""

    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=request.data['username'])
            if User.check_confirmation_code(
                self, user.confirmation_code,
                serializer.data['confirmation_code']
            ):
                user.is_active = True
                user.save()
                get_token(self, user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
