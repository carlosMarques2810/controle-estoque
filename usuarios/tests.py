from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Login

Usuario = get_user_model()

class UsuarioTest(APITestCase):
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
        url = f"/api/usuarios/{user1.id}/configuracao/"
        response = self.client.patch(url, {'pode_adicionar_produto': True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verificando se o superuser pode mudar as suas proprias permissões
        url = f"/api/usuarios/{gerente.id}/configuracao/"
        response = self.client.patch(url, {'pode_adicionar_produto': False}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verificando se o usuario pode alterar as suas proprias permissões
        self.client.force_authenticate(user=user1)
        url = f"/api/usuarios/{user1.id}/configuracao/"
        response = self.client.patch(url, {'pode_adicionar_produto': True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Você não tem permissão para executar essa ação.")

    def test_login_e_logins_de_acesso_e_refresh_token(self):
        from decouple import config
        # verifica o login
        response = self.client.post("/api/auth/login", {"email": config("SUPERUSER_EMAIL"), "password": config("SUPERUSER_PASSWORD")}, format="json")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsNotNone(response.data["access"])

        # verificando log de acessos
        self.assertEqual(Login.objects.count(), 1)
        self.assertEqual(Login.objects.filter(usuario=Usuario.objects.first()).exists(), True)

        #renovação do token 
        refresh = response.data['refresh']
        response = self.client.post("/api/auth/refresh/", {"refresh": refresh}, format="json")
        self.assertIn("access", response.data)
        self.assertIsNotNone(response.data["access"])