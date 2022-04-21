from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import (MAX_SCORE, MIN_SCORE, Category, Comment, Genre,
                            Review, Title, User)
from reviews.validators import year_validator


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    confirmation_code = serializers.CharField(required=True, max_length=100)

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = username = data.get('confirmation_code')

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Код неверен')
        return data

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class GetConfirmationCode(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Выберите другое имя')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True, default=serializers.CurrentUserDefault())

    title = serializers.HiddenField(default=0)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    score = serializers.IntegerField(
        validators=[
            MaxValueValidator(
                MAX_SCORE, 'Выберите значение от 1 до 10'),
            MinValueValidator(
                MIN_SCORE, 'Выберите значение от 1 до 10'),
        ]
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        request = self.context['request']
        author = request.user
        if request.method == 'POST':
            if Review.objects.filter(author=author, title=title).exists():
                raise ValidationError('Нельзя добавлять более одного'
                                      'отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, max_length=150, validators=[
            UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        required=True, max_length=254, validators=[
            UniqueValidator(queryset=User.objects.all())])
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES, default=User.USER)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'bio')


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'bio')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[year_validator],)

    class Meta:
        model = Title
        fields = '__all__'


class ReadTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'
