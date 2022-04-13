from audioop import avg
import statistics
from django.db import models
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, status, action
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title, User
from .permissions import (IsAdminOrReadOnly, 
                          IsAdminModeratorAuthorOrReadOnly, IsAdmin,)
from .serializers import (CommentSerializer, ReviewSerializer, UserSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,) 


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer

    @action(detail=False,
            methods=['get','patch',],
        ) # может url_path='profile'
    def user_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user) # может можно по-другому
            return Response(status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset_new = title.reviews.all()
        return queryset_new

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ...


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    ...