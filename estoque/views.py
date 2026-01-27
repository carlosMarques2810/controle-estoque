from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Fornecedor, Produto
from .serializer import FornecedorSerializer, ProdutoSerializer, ListProdutosDistintos
from .permission import FornecedorTemPermissao, ProdutoTemPermissao

class FornecedorViewSet(ModelViewSet):
    queryset = Fornecedor.objects.prefetch_related("produtos")
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated, FornecedorTemPermissao]

    @action(detail=True, methods=["GET"], url_name="produtos", url_path="produtos")
    def produtos(self, request, pk=None):
        fornecedor = self.get_object()
        produtos = fornecedor.produtos.values("codigo", "nome", "categoria").distinct()
        serializer = ListProdutosDistintos(produtos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.select_related("fornecedor")
    serializer_class =  ProdutoSerializer
    permission_classes = [IsAuthenticated, ProdutoTemPermissao]