from rest_framework import serializers
from .models import Fornecedor, Produto
from django.db.models import Sum
from django.utils import timezone

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ["id", "razao_social", "nome_fantasia", "inscricao_estadual", "endereco", "municipio", "email", "telefone"]

# Usado pra simplificar os dodos de fonecedores em produtos
class FornecedorResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ["id", "nome_fantasia", "email"]

class ProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer responsável pela criação e representação de produtos em estoque.

    Regras de negócio aplicadas:

    1) Controle de estoque por lote e validade
    -----------------------------------------
    Cada registro de Produto representa um lote específico de um produto,
    identificado pela combinação:
        - código
        - lote
        - vencimento
        - fornecedor

    Caso um produto com essa mesma combinação já exista no banco de dados,
    o sistema NÃO cria um novo registro. Em vez disso:
        - soma a quantidade informada à quantidade já existente
        - preserva a integridade do estoque

    Essa lógica evita duplicação de registros do mesmo lote e garante
    consistência nos cálculos de estoque.
    """
    fornecedor = FornecedorResumoSerializer(read_only=True)
    quantidate_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Produto
        fields = ["id", "nome", "codigo", "categoria", "lote", "vencimento", "quantidate", "valor_unitario", "fornecedor"]

    def get_quantidade_total(self, obj):
        """
        Retorna a quantidade total disponível do produto no estoque.

        Observações importantes:
        - A quantidade real do produto NÃO está em um único registro
        - Ela é calculada como a soma das quantidades de todos os registros que compartilham o mesmo código
        - Cada registro pode representar um lote e validade diferentes

        Implementação:
        - Filtra todos os produtos com o mesmo código
        - Soma o campo 'quantidade' no banco de dados dos produtos não vencidos
        - Retorna 0 caso não existam registros
        """
        return Produto.objects.filter(
            codigo=obj.codigo,
            vencimento__gte=timezone.now()
        ).aggregate(
            total=Sum("quantidade")
        )["total"] or 0

    def create(self, validated_data):
        """
        Sobrescreve o método create padrão do DRF para aplicar a regra
        de atualização de estoque por lote.

        Fluxo:
        1) Verifica se já existe um produto com o mesmo:
           - código
           - lote
           - vencimento
           - fornecedor

        2) Se existir:
           - soma a quantidade recebida à quantidade atual
           - retorna o registro existente

        3) Se não existir:
           - cria um novo registro de produto normalmente
        """
        produto = Produto.objects.filter(
            codigo=validated_data["codigo"],
            lote=validated_data["lote"],
            vencimento=validated_data["vencimento"],
            fornecedor=validated_data["fornecedor"],
        ).first()

        if produto:
            produto.quantidade += validated_data["quantidade"]
            produto.save()
            return produto

        return super().create(validated_data)
    
# serializer para listar os produtos com nome, codigo e categoria, para a rota /api/fornecedore/{id}/produtos/, de forma distinta
class ListProdutosDistintos(serializers.Serializer):
    codigo = serializers.CharField(read_only=True)
    nome = serializers.CharField(read_only=True)
    categoria = serializers.CharField(read_only=True)