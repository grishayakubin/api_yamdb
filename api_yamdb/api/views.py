from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title

from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleViewSerializer,
)


class CategoryViewSet(ModelViewSet):
    """
    Класс-контроллер для обработки запросов, относящихся к категориям.

    Атрибуты:
    - queryset: набор всех объектов модели Categories.
    - serializer_class: класс сериализатора CategoriesSerializer.
    - permission_classes: список классов разрешений для доступа к данным.
        Добавить категорию может только админ, просматривать могут все.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class GenreViewSet(ModelViewSet):
    """
    Класс-контроллер для обработки запросов, относящихся к жанрам.

    Атрибуты:
    - queryset: набор всех объектов модели Genres.
    - serializer_class: класс сериализатора GenresSerializer.
    - permission_classes: список классов разрешений для доступа к данным.
        Добавить жанр может только админ, просматривать могут все.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly, )


class TitleViewSet(ModelViewSet):
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
    get_serializer_class(): выбор сериализатора в зависимости от типа запроса.
    """

    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'genre']
    ordering_fields = ['-pub_date']
    http_method_names = ['get', 'post', 'delete', 'patch']

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

    def get_serializer_class(self):
        '''
        Если запрос является запросом на чтение списка объектов
        или одного объекта, то используется "TitleViewSerializer",
        если нет, то "TitleSerializer".
        '''
        if self.action in ("list", "retrieve"):
            return TitleViewSerializer
        return TitleSerializer
