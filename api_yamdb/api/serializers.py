from rest_framework import serializers
from django.db.models import Avg
from reviews.models import Category, Comment, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'score', 'title', 'author', 'pub_date')
        model = Review
        read_only_fields = ('author', 'pub_date', 'id', 'text')

    def validate_score(self, value):
        if value not in [0, 10]:
            raise serializers.ValidationError(
                'Вы можете поставить оценку от 0 до 10'
            )
        return value



class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

    def validate_name(self, value):
        """
        Проверяет длину названия категории.
        """
        if len(value) < 5:
            raise serializers.ValidationError(
                'Длина названия должна составлять не менее 5 символов.'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    """

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')

    def validate_name(self, value):
        """
        Проверяет длину названия жанра.
        """
        if len(value) < 5:
            raise serializers.ValidationError(
                'Длина названия должна составлять не менее 5 символов.'
            )
        return value


class TitleViewSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Title на чтение данных.'''

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']


class TitleSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Title на запись данных.'''

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'year',
            'category',
            'genre'
        )
        model = Title