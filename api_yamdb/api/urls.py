from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    get_confirmation_code, get_token)

router_version_1 = routers.DefaultRouter()


router_version_1.register(r'categories', CategoryViewSet)
router_version_1.register(r'genres', GenreViewSet)
router_version_1.register(r'titles', TitleViewSet)
router_version_1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_version_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_version_1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', get_token, name='token_obtain_pair'),
    path('v1/auth/signup/', get_confirmation_code, name='get_conf_code'),
    path('v1/', include(router_version_1.urls)),
]
