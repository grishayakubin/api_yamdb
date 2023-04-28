from django.shortcuts import get_object_or_404
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Comment, Genre, Review, Title

from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


class CategoryViewSet(ModelViewSet):
    pass


class GenreViewSet(ModelViewSet):
    pass


class TitleViewSet(ModelViewSet):
    pass


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.annotate(rating=Avg('score'))
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()
