#codigo 6
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    # Ruta para obtener un token de acceso y un token de renovación.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Ruta para refrescar el token de acceso usando un token de renovación válido.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]