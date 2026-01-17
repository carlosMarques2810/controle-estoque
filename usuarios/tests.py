from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioTest(APITestCase):
    def setUp(self):
        self.gerente_dados = {
            'nome_do_usuario': "gerente.nome",
            'email': "gerente@email.com",
            'senha': "gerente123",
            'confirmar_senha': "gerente123"
        }

        self.gerido_dados = {
            'nome_do_usuario': "gereido.nome",
            'email': "gereido@email.com",
            'senha': "gereido123",
            'confirmar_senha': "gereido123"
        }

    def test_regra_de_registro(self):
        # Registro dos gerentes acontece com os que não estão autenticados
        url = reverse("usuario-list")
        response = self.client.post(url, self.gerente_dados, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Usuario.objects.first().is_gerente, True)
        self.assertEqual(Usuario.objects.first().gerente, None)

        # Grentes desgnando seu geridos
        self.client.force_authenticate(user=Usuario.objects.first())
        response = self.client.post(url, self.gerido_dados, format="json")
        self.assertEqual(Usuario.objects.count(), 2)
        self.assertEqual(Usuario.objects.filter(id=response.data['id']).first().is_gerente, False)
        self.assertEqual(Usuario.objects.filter(id=2).first().gerente, Usuario.objects.first())

    def test_apenas_gerente_define_acoes_no_estoque(self):
        url = reverse("usuario-list")
        response = self.client.post(url, self.gerente_dados, format="json")
        gerente = Usuario.objects.first()
        self.client.force_authenticate(user=gerente)
        response = self.client.post(url, self.gerido_dados, format="json")
        gerido = Usuario.objects.last()

        # Verificado se o gerente pode alterar as permissiões dos seus geridos
        url = f"/api/usuarios/{gerido.id}/configuracao/"
        response = self.client.patch(url, {'pode_adicionar_produto': True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verificando se o gerente pode mudar as suas proprias permissões
        url = f"/api/usuarios/{gerente.id}/configuracao/"
        response = self.client.patch(url, {'pode_adicionar_produto': False}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verificando se o gerido pode alterar as suas proprias permissões
        self.client.force_authenticate(user=gerido)
        url = f"/api/usuarios/{gerido.id}/configuracao/"
        response = self.client.patch(url, {'pode_adicionar_produto': True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Você não tem permissão para executar essa ação.")

    def test_login_e_refresh_token(self):
        # usuario do teste de login
        url = reverse("usuario-list")
        self.client.post(url, self.gerente_dados, format="json")
        Usuario.objects.first()
    
        # verifica o login
        response = self.client.post("/api/auth/login", {"email": self.gerente_dados['email'], "password": self.gerente_dados['senha']}, format="json")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsNotNone(response.data["access"])

        #renovação do token 
        refresh = response.data['refresh']
        response = self.client.post("/api/auth/refresh/", {"refresh": refresh}, format="json")
        self.assertIn("access", response.data)
        self.assertIsNotNone(response.data["access"])