from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .permissions import (IsAdminOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly, IsAdmin,)
from .serializers import (CommentSerializer, ReviewSerializer, UserSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer,
                          GetTokenSerializer, GetConfirmationCode,
                          MeSerializer, ReadTitleSerializer)
from .pagination import UserPagination
from .filtres import TitleFilter


@api_view(['POST'])
@permission_classes([AllowAny],)
def get_confirmation_code(request):
    if request.method == 'POST':
        serializer = GetConfirmationCode(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Title: Please, use it code for generate token',
                f'{confirmation_code}',
                'artem@gmail.com',
                [request.data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny],)
def get_token(request):
    if request.method == 'POST':
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    username=serializer.validated_data.get('username'))
            except User.DoesNotExist:
                return Response(
                    serializer.errors, status=status.HTTP_404_NOT_FOUND)
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return ReadTitleSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = UserPagination

    @action(detail=False,
            methods=['get', 'patch', ],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
class MeView(views.APIView):

    @permission_classes([IsAuthenticated],)
    def get(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated],)
    def patch(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = MeSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset_new = title.reviews.all()
        return queryset_new

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset_new = review.comments.all()
        return queryset_new

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
