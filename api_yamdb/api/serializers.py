from rest_framework import serializers

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
