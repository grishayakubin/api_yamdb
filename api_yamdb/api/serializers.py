from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Categories.
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
    Сериализатор для модели Genres.
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


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Titles.
    """

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
            'rating'
        )

    def validate_slug(self, value):
        """
        Проверяет, что slug для произведения уникален.
        """
        if Title.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Произведение с таким slug уже существует.'
            )
        return value
