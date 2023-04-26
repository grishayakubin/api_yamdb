from rest_framework import serializers

from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Categories.
    """

    class Meta:
        model = Categories
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


class GenresSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genres.
    """

    class Meta:
        model = Genres
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


class TitlesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Titles.
    """

    class Meta:
        model = Titles
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
        if Titles.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Произведение с таким slug уже существует.'
            )
        return value
