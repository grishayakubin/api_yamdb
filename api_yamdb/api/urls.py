from rest_framework import routers
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import GetAuthTokenView, signup, UserViewSet
from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = "api"

v1_router = DefaultRouter()
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
routers.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(routers.urls)),
    path("v1/auth/signup/", signup, name="sign_up"),
    path("v1/auth/token/", GetAuthTokenView.as_view(), name="get_token"),
]
