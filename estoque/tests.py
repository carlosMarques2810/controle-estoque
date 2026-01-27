from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Fornecedor, Produto

Usuario = get_user_model()

class Fornecedor_produto_test(APITestCase):
    def setUp(self):
        self.gerente = Usuario.objects.first()
        # usuário comun == sem permissões especificas para lidar com produtos e fornecedores
        self.usuario_comun = Usuario.objects.create(username="usuario_comun", email="usuario@comun.com", password="usuariocomun")

        self.fornecedor = Fornecedor.objects.create(
            razao_social="Distribuidora Alfa LTDA",
            nome_fantasia="Alfa Distribuição",
            inscricao_estadual="123456789",
            endereco="Rua das Flores, 123",
            municipio="Manaus",
            email="contato@alfadistribuicao.com",
            telefone="(92) 99999-0000"
        )

        self.produto = Produto.objects.create(
            nome="Arroz Tipo 1",
            codigo="ARZ001",
            categoria="Alimentos",
            lote="L2026A",
            vencimento="2026-12-31",
            quantidade=100,
            valor_unitario=7.50,
            Fornecedor=self.fornecedor
        )
    # verifica as pemissões especificar para lidar com os fornecedores
    def test_fornecedor_permissoes(self):
        fornecedor_dado = {
            "razao_social": "Distribuidora Alfa LTDA",
            "nome_fantasia": "Alfa Distribuição",
            "inscricao_estadual": "123456789",
            "endereco": "Rua das Flores, 123",
            "municipio": "Manaus",
            "email": "contato@alfadistribuicao.com",
            "telefone": "(92) 99999-0000"
        }

        self.client.force_authenticate(user=self.usuario_comun)

        # cadastrar fornecedor
        url = reverse("fornecedor-list")
        response = self.client.post(url, data=fornecedor_dado, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # editar fornecedor
        url = reverse("fornecedor-detail", kwargs={"pk": self.fornecedor.id})
        response = self.client.put(url, data=fornecedor_dado, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # deletar fornecedor
        url = reverse("fornecedor-detail", kwargs={"pk": self.fornecedor.id})
        response = self.client.delete(url, data=fornecedor_dado, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # verifica as pemissões especificar para lidar com os produtos
    def test_fornecedor_permissoes(self):
        produto_dado = {
            "nome": "Arroz Tipo 1",
            "codigo": "ARZ001",
            "categoria": "Alimentos",
            "lote": "L2026A",
            "vencimento": "2026-12-31",
            "quantidade": 100,
            "valor_unitario": "7.50",
            "fornecedor": self.fornecedor.id
        }

        self.client.force_authenticate(user=self.usuario_comun)

        # cadastrar produto
        url = reverse("produto-list")
        response = self.client.post(url, data=produto_dado, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # editar produto
        url = reverse("produto-detail", kwargs={"pk": self.produto.id})
        response = self.client.put(url, data=produto_dado, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # deletar produto
        url = reverse("produto-detail", kwargs={"pk": self.produto.id})
        response = self.client.delete(url, data=produto_dado, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)