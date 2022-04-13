from django.urls import include, path
from rest_framework import routers


router_version_1 = routers.DefaultRouter()

# router_version_1 = register(r'', ViewSet)

urlpatterns = [
    path('v1/', include(router_version_1.urls))
]

#urlpatterns = [
#    ...
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
#    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
#    path('auth/', include('djoser.urls.jwt')),
#]