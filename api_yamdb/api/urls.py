<<<<<<< HEAD
=======
from django.urls import include, path
from rest_framework import routers

from .views import (get_confirmation_code, get_token, CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, MeView)

router_version_1 = routers.DefaultRouter()

# router_version_1 = register(r'', ViewSet)
router_version_1.register(r'categories', CategoryViewSet)
router_version_1.register(r'genres', GenreViewSet)
router_version_1.register(r'titles', TitleViewSet)
router_version_1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_version_1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router_version_1.register(r'users', UserViewSet)

#urlpatterns = [
#    path('v1/auth/token/', get_token, name='token_obtain_pair'),
#    path('v1/auth/signup/', get_confirmation_code, name='get_conf_code'),
#    path('v1/', include(router_version_1.urls))
#]

router_version_1.register(r'users/me/', MeView, basename='users_me')
#router_version_1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', get_token, name='token_obtain_pair'),
    path('v1/auth/signup/', get_confirmation_code, name='get_conf_code'),
    path('v1/users/me/', MeView.as_view()),
    path('v1/', include(router_version_1.urls)),
]
>>>>>>> b7011c7f76b7ea4c0238f6d92959130bd5dc52b5
