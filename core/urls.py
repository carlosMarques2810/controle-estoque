from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios import views as u_views
from estoque import views as e_views

router = DefaultRouter()
router.register(r"usuarios", u_views.UsuarioViewSet, basename="usuario")
router.register(r"fornecedores", e_views.FornecedorViewSet, basename="fornecedor")
router.register(r"produtos", e_views.ProdutoViewSet, basename="produto")
router.register(r"auth", u_views.RecuperacaoViewSet, basename="auth")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login', u_views.LoginView.as_view(), name="obter_token"),
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
#     POST

# api/auth/refresh/
#     POST

# /api/auth/recuperar/
#     POST

# api/auth/recuperar/confirmar/?token=
#     POST

# /api/fornecedore/
#     GET
#     POST

# /api/fornecedores/{id}/
#     GET
#     PUT
#     PATCH
#     DELETE

# /api/fornecedores/{id}/produtos/
#     GET

# /api/produtos/
#     GET
#     POST

# /api/produtos/{id}/
#     GET
#     PUT
#     PATCH
#     DELETE