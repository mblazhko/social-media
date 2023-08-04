from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets

from content.models import Post
from content.serializers import PostSerializer, PostListSerializer
from user.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    @staticmethod
    def _params_to_ints(qs) -> list[int]:
        return [int(str_id) for str_id in qs.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def get_queryset(self):
        user = self.request.user
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        created_at = self.request.query_params.get("created_at")
        hashtags = self.request.query_params.get("hashtags")

        queryset = self.queryset

        if user.is_authenticated:
            queryset = queryset.filter(
                Q(owner=user) | Q(owner__in=user.followings.all())
            )

        if first_name and last_name:
            queryset = queryset.filter(
                Q(owner__first_name=first_name) & Q(owner__last_name=last_name)
            )

        if created_at:
            date = datetime.strptime(created_at, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__date=date)

        if hashtags:
            hashtags_ids = self._params_to_ints(hashtags)
            queryset = queryset.filter(hashtags__id__in=hashtags_ids)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
