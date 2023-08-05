from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from user.permissions import IsOwnerOrReadOnly
from user.serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserListSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[
            AllowAny,
        ],
    )
    def upload_image(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageUserView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.request.user

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[
            IsOwnerOrReadOnly,
        ],
    )
    def upload_image(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset.distinct()


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            access_token = request.data["access_token"]

            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()

            access_token_obj = RefreshToken(access_token)
            access_token_obj.blacklist()

            return Response(
                {"detail": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
