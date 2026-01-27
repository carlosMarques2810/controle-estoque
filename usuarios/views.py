from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializer import UsuarioSerializer, LoginSerilaizer, ConfiguracaoSerializer, LogsAcessoSerializer, EncontrarUsuarioSerializer
from .permission import UsuarioTemPermissao
from .models import Recuperacao
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
import secrets

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
    
    @action(detail=True, methods={'get'}, url_name="login-logs", url_path="login-logs")
    def login_logs(self, request, pk=None):
        """
        Retorna o histórico de login do usuário
        """
        usuario = self.get_object()
        serilizer = LogsAcessoSerializer(usuario.acessos.all(), many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get', 'put', 'patch'], url_name="permissoes", url_path="permissoes")
    def permissoes(self, request, pk=None):
        """
        Visualiza ou atualiza permissões do usuário
        """
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

class RecuperacaoViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_name="recuperar", url_path="recuperar")
    def recuperar(self, request):
        serializer = EncontrarUsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        usuario = Usuario.objects.get(email=email)
        token = get_random_string(64)

        Recuperacao.objects.create(
            usuario=usuario, 
            token=token,
            expiracao=timezone.now() + timezone.timedelta(minutes=30)
        )

        link = f"https://localhost:8000/recuperacao/confirmar/?token={token}"
        mensagem =  f"""Olá,\n\n
        Recebemos uma solicitação de recuperação de acesso à sua conta.\n\n
        Para continuar o processo, clique no link abaixo:\n\n
        {link}\n\n"
        Este link é válido por tempo limitado.\n\n
        Caso você NÃO tenha solicitado a recuperação de acesso,
        recomendamos que entre em contato com a gerência ou
        com o suporte do sistema imediatamente.\n\n"
        Atenciosamente,\n
        Equipe do Sistema"""

        send_mail(
            subject="Recuperação de acesso.",
            message=mensagem,
            from_email=None,
            recipient_list=[email],
        )

        return Response({"detail": "Se o e-mail estiver cadastrado, você receberá as instruções de recuperação."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_name="recuperar-confirmar", url_path="recuperar/confirmar")
    def confirmar(self, request):
        token = request.query_params.get("token")

        if not token:
            return Response(
                {"detail": "Token não informado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        recuperacao = Recuperacao.objects.filter(
            token=token,
            expiracao__gte=timezone.now()
        ).first()

        if not recuperacao:
            return Response(
                {"detail": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        nova_senha = secrets.token_urlsafe(8)

        usuario = recuperacao.usuario
        usuario.set_password(nova_senha)
        usuario.save()

        send_mail(
            subject="Nova senha de acesso",
            message=f"Sua nova senha é: {nova_senha}",
            from_email=None,
            recipient_list=[usuario.email],
        )

        recuperacao.delete()

        return Response(
            {"detail": "Nova senha enviada para o e-mail."},
            status=status.HTTP_200_OK
        )