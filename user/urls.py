from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import (
    CreateUserView,
    ManageUserView,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register("users", UserViewSet)


app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "me/",
        ManageUserView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "post": "upload_image",
            }
        ),
        name="manage",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
