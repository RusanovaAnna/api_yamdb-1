from django.urls import include, path
from rest_framework import routers

from .views import get_confirmation_code, get_token

router_version_1 = routers.DefaultRouter()

# router_version_1 = register(r'', ViewSet)

urlpatterns = [
    path('v1/auth/token/', get_token, name='token_obtain_pair'),
    path('v1/auth/signup/', get_confirmation_code, name='get_conf_code'),
    path('v1/', include(router_version_1.urls))
]
