from django.db import models
from django.contrib.auth.models import User

# relatorio
class Relatorio(models.Model):
    class TipoRelatorio(models.TextChoices):
        USUARIOS = "usuarios", "Usuários"
        PRODUTOS = "produtos", "Protutos"
        FORNECEDOR = "fornecedor", "Fornecedor"

    usuario = models.ForeignKey(User, related_name="relatorios", on_delete=models.CASCADE)
    tipo_relatorio = models.CharField(max_length=20, choices=TipoRelatorio.choices)
    data_gerecao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_relatorio_display()} - {self.data_gerecao:%d/%m%Y}"
    
    class Meta:
        db_table = "relatorio"