from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault


from .models import User, Category, Genre, Title, Comments, Review


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        many=True,
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
        )
        model = Title


class TitleViewSerializer(TitleSerializer):
    rating = serializers.FloatField(
        read_only=True
    )
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta(TitleSerializer.Meta):
        fields = TitleSerializer.Meta.fields + ('rating', )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            author = self.context.get('author')
            title = self.context.get('title')
            if Review.objects.filter(author=author, title=title).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв к данной публикации'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
