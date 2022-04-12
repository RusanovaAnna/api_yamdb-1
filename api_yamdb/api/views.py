from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from reviews.models import Category, Genre, Review, Title, User
from .permissions import (IsAdminOrReadOnly, 
                          IsAdminModeratorAuthorOrReadOnly, IsAdmin,)
from .serializers import (CommentSerializer, ReviewSerializer, UserSerializer)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    ):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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

    def user_profile():
        ...


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        queryset_new = title.reviews.all()
        return queryset_new

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    
    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        queryset_new = review.comments.all()
        return queryset_new

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    ...


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt_token(request):
    ...