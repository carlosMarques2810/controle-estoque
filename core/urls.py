from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios import views

router = DefaultRouter()
router.register(r"usuarios", views.UsuarioViewSet, basename="usuario")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login', views.LoginView.as_view(), name="obter_token"),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name="atualizar_token")
]


# /api/usuarios/
#     GET
#     POST

# /api/usuarios/{id}/
#     GET
#     PUT
#     PATCH
#     DELETE

# /api/usuarios/{id}/permissoes/
#     GET
#     PUT
#     PATCH

# /api/usuarios/{id}/login-logs/
#     GET

# /api/auth/login/
# api/auth/refresh/
