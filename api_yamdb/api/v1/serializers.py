from rest_framework import serializers
from reviews.models import Comments, Review
from rest_framework.serializers import ModelSerializer, IntegerField
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title

User = get_user_model()


class UserCreationSerializer(serializers.Serializer):
    """Сериализация для регистрации."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Валидация email."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Такой пользователь с указаннной {email} сущ.'
            )
        return value

    def validate_username(sefl, value):
        """Валидация username."""
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(
                'Пользователь с me недоступен.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Такой пользователь с указаннной {username} сущ.'
            )
        return value


class UserAuthSerializer(serializers.Serializer):
    """Скриализация для аутенфикации по токену."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, data):
        """Валидация confirmation_code."""
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token


class UserSerializers(serializers.ModelSerializer):
    """Скриализация для пользователей."""

    class Meta:
        """Класс Meta."""

        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'role',
            'email'
        )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GengreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'category',
            'genre',
            'description',
            'year'
        )


class TitleReadSerializer(ModelSerializer):
    genre = GengreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'category',
            'genre',
            'description',
            'year',
            'rating'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id')

    class Meta:
        model = Review
        fields = ('title', 'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Возможен один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
