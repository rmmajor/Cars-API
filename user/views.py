from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from django.contrib.auth.models import User
from .serializers import RegistrationSerializer


class UserView(GenericViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(methods=['post'], url_path="create", detail=False, permission_classes=[AllowAny])
    def registration(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
