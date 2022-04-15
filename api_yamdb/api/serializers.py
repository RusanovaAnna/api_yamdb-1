from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Comment, Review, User, Category, Title, Genre


class GetTokenSerializer(serializers.ModelSerializer):

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

    def validate_username(self, val):
        if 'me' in val.lower():
            raise serializers.ValidationError()
        return val
        #user = User.query.filter_by(username='me').first()
        #if user:
        #    raise serializers.ValidationError()

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
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'bio')


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'bio')
        read_only_fields = ('role',)
        model = User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


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

    class Meta:
        fields = '__all__'
        model = Title
