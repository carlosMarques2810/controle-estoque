from django.db import models
from django.conf import settings

# fornecedor
class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=150)
    inscricao_estadual = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    municipio = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_fantasia
    
    class Meta:
        db_table = "fornecedores"

# produto
class Produto(models.Model):
    gerente = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={"is_gerente": True}, on_delete=models.PROTECT)
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    lote = models.CharField(max_length=50)
    vencimento = models.DateField()
    qauntidade = models.PositiveBigIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    Fornecedor = models.ForeignKey(Fornecedor, related_name="produtos", on_delete=models.PROTECT)

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = "produtos"