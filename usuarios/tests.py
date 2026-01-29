from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Login, Recuperacao
from django.core import mail

Usuario = get_user_model()

class Usuario_test(APITestCase):
    def setUp(self):
        self.user1_dados = {
            'nome_do_usuario': "user1.nome",
            'email': "user1@email.com",
            'senha': "user1123",
            'confirmar_senha': "user1123"
        }

        self.user2_dados = {
            'nome_do_usuario': "user2.nome",
            'email': "user2@email.com",
            'senha': "user2123",
            'confirmar_senha': "user2123"
        }

    def test_regra_de_registro(self):
        url = reverse("usuario-list")

        # verificando se o superuser foi criado
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Usuario.objects.first().is_superuser, True)

        # criação de usuario pelo superuser
        self.client.force_authenticate(user=Usuario.objects.first())
        response = self.client.post(url, self.user1_dados, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 2)

        # criação de usuario por outro comun
        self.client.force_authenticate(user=Usuario.objects.last())
        response = self.client.post(url, self.user2_dados, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_apenas_superuser_define_acoes_no_estoque(self):
        user1 = Usuario.objects.create_user(username="user1.username", email="user1@email.com", password="user1234")
        gerente = Usuario.objects.first()
        self.client.force_authenticate(user=gerente)

        # Verificado se o superuser pode alterar as permissiões dos seus geridos
        url = reverse("usuario-permissoes", kwargs={"pk": user1.id})
        response = self.client.patch(url, {'pode_adicionar_produto': True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verificando se o superuser pode mudar as suas proprias permissões
        url = reverse("usuario-permissoes", kwargs={"pk": gerente.id})
        response = self.client.patch(url, {'pode_adicionar_produto': False}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verificando se o usuario pode alterar as suas proprias permissões
        self.client.force_authenticate(user=user1)
        url = reverse("usuario-permissoes", kwargs={"pk": user1.id})
        response = self.client.patch(url, {'pode_adicionar_produto': True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Você não tem permissão para executar essa ação.")

    def test_login_e_logins_de_acesso_e_refresh_token(self):
        from decouple import config
        # verifica o login
        url = reverse("obter-token")
        response = self.client.post(url, {"email": config("SUPERUSER_EMAIL"), "password": config("SUPERUSER_PASSWORD")}, format="json")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsNotNone(response.data["access"])

        # verificando log de acessos
        self.assertEqual(Login.objects.count(), 1)
        self.assertEqual(Login.objects.filter(usuario=Usuario.objects.first()).exists(), True)

        #renovação do token 
        url = reverse("atualizar-token")
        refresh = response.data['refresh']
        response = self.client.post(url, {"refresh": refresh}, format="json")
        self.assertIn("access", response.data)
        self.assertIsNotNone(response.data["access"])

    def test_recuperacao_acesso(self):
        gerente = Usuario.objects.first()

        # verificando o envio de e-mail de recuperação
        url = reverse("auth-recuperar")
        self.client.force_authenticate(user=gerente)
        response = self.client.post(url, data={"email": gerente.email}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.data["detail"], "Se o e-mail estiver cadastrado, você receberá as instruções de recuperação.")

        # verificando a confimação de recuperação de acesso
        recuperacao = Recuperacao.objects.filter(usuario=gerente).first()
        url = f"{reverse("auth-recuperar-confirmar")}?token={recuperacao.token}"
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(response.data["detail"], "Nova senha enviada para o e-mail.")
        self.assertFalse(Recuperacao.objects.filter(usuario=gerente).exists())
        # verificar a lsita de e-mail enviados
        # mail.outbox[1].body
