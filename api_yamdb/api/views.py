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


class CategoriesViewSet(ModelViewSet):
    """
    Класс-контроллер для обработки запросов, относящихся к категориям.

    Атрибуты:
    - queryset: набор всех объектов модели Categories.
    - serializer_class: класс сериализатора CategoriesSerializer.
    - permission_classes: список классов разрешений для доступа к данным.
        Добавить категорию может только админ, просматривать могут все.
    """

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class GenresViewSet(ModelViewSet):
    """
    Класс-контроллер для обработки запросов, относящихся к жанрам.

    Атрибуты:
    - queryset: набор всех объектов модели Genres.
    - serializer_class: класс сериализатора GenresSerializer.
    - permission_classes: список классов разрешений для доступа к данным.
        Добавить жанр может только админ, просматривать могут все.
    """

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class TitlesViewSet(ModelViewSet):
    """
    Класс-контроллер для обработки запросов, относящихся к произведениям.

    Атрибуты:
    - queryset: набор всех объектов модели Titles.
        Метод select_related() используется для предварительной загрузки
        связанных объектов в одном запросе к базе данных.
    - serializer_class: класс сериализатора TitlesSerializer.
    - permission_classes: список классов разрешений для доступа к данным.
        Добавить произведение может только админ, просматривать могут все.
    - pagination_class: класс пагинации LimitOffsetPagination.
    - filter_backends: список классов фильтрации и сортировки.
    - filterset_fields: список полей для фильтрации.
    - ordering_fields: список полей для сортировки.

    Методы:
    get_queryset(): получение отфильтрованного и отсортированного queryset.
    """

    queryset = Titles.objects.select_related('author')
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'genre']
    ordering_fields = ['pub_date']

    def get_queryset(self):
        """
        Получение отфильтрованного и отсортированного queryset.

        Аргументы:
        - self: экземпляр класса TitlesViewSet.

        Возвращает:
        - queryset: отфильтрованный и отсортированный queryset.
        """
        queryset = super().get_queryset()

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        return queryset
