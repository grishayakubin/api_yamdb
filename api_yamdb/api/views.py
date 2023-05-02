from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, CharFilter, FilterSet
from rest_framework import filters, status, viewsets
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .registration.confirmation import send_confirmation_code
from .registration.token_generator import get_token_for_user
from .serializers import (
    GetAuthTokenSerializer,
    SignUpSerializer,
    UserProfileSerializer,
    UserSerializer,
)
from api.permissions import (
    IsAdmin, IsAdminOrReadOnly,
    IsAuthorModeratorAdminOrReadOnly,
)
from reviews.models import Category, Genre, Review, Title
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleRetrieveSerializer,
    TitleWriteSerializer,
)
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)


class GetListCreateDeleteMixin(
    GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin
):
    """Кастомный класс для жанров и категорий."""

    pass


class TitleFilter(FilterSet):
    category = CharFilter(field_name="category__slug", lookup_expr="iexact")
    genre = CharFilter(field_name="genre__slug", lookup_expr="iexact")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = "__all__"


class ReviewViewSet(ModelViewSet):
    """
    Получить список всех отзывов.
    Добавление нового отзыва.
    Получение отзыва по id.
    Обновление отзыва по id.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    http_method_names = ("get", "post", "delete", "patch")

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    """
    Получить список всех комментариев.
    Добавление нового комментария к отзыву.
    Получить комментарий по id.
    Обновление комментария по id.
    Удаление комментария.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    http_method_names = ("get", "post", "delete", "patch")

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведения."""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ("get", "post", "delete", "patch")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleRetrieveSerializer
        return TitleWriteSerializer


class CategoryViewSet(GetListCreateDeleteMixin):
    """Вьюсет для категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(GetListCreateDeleteMixin):
    """Вьюсет для жанра."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class UserViewSet(ModelViewSet):
    """Вьюсет модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ("get", "post", "delete", "patch")

    @action(
        detail=False,
        methods=("get", "patch"),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UserProfileSerializer(
            request.user, partial=True, data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    email = serializer.data["email"]
    username = serializer.data["username"]

    user, _ = User.objects.get_or_create(email=email, username=username)

    user.confirmation_code = send_confirmation_code(user)
    user.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


class GetAuthTokenView(APIView):
    """CBV для получения и обновления токена."""

    def post(self, request):
        serializer = GetAuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {"confirmation_code": ["Неверный код подтверждения"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(get_token_for_user(user), status=status.HTTP_200_OK)
