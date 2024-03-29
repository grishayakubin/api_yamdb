from rest_framework import routers
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


v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path("v1/auth/signup/", signup, name="sign_up"),
    path("v1/auth/token/", GetAuthTokenView.as_view(), name="get_token"),
]
