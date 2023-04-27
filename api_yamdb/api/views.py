
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Categories, Genres, Titles

from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
)


class CategoryViewSet(ModelViewSet):
    pass


class GenreViewSet(ModelViewSet):
    pass


class TitleViewSet(ModelViewSet):
    pass


class ReviewViewSet(ModelViewSet):
    pass


class CommentViewSet(ModelViewSet):
    pass
