from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializer import UsuarioSerializer, LoginSerilaizer, ConfiguracaoSerializer, LogsAcessoSerializer, RecuperacaoSerializer
from .permission import UsuarioTemPermissao

Usuario = get_user_model()

class UsuarioViewSet(ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, UsuarioTemPermissao]

    def get_queryset(self):
        user = self.request.user
        queryset = Usuario.objects.select_related("configuracao")

        if not user.is_authenticated:
            return Usuario.objects.none()

        if user.configuracao.permissao_total or user.configuracao.acesso_configuracao_sistema:
            return queryset

        return queryset.filter(id=user.id)
    
    @action(detail=True, methods={'get'})
    def logins(self, request, pk=None):
        usuario = self.get_object()
        serilizer = LogsAcessoSerializer(usuario.acessos.all(), many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get', 'put', 'patch'])
    def configuracao(self, request, pk=None):
        usuario = self.get_object()
        configuracao = usuario.configuracao
        
        if request.method == "GET":
            serializer = ConfiguracaoSerializer(configuracao)
            Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        serializer = ConfiguracaoSerializer(
            configuracao,
            data=request.data,
            partial=(request.method == "PATCH")
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerilaizer