from django.db import models
from django.contrib.auth.models import User

# login
class Login(models.Model):
    usuario = models.ForeignKey(User, related_name="usuario", on_delete=models.CASCADE)
    data_login = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.email} - {self.data_login}"
    
    class Meta:
        db_table = "login"

# recuperação
class Recuperacao(models.Model):
    usuario = models.ForeignKey(User, related_name="recuperacao", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiracao = models.DateTimeField()

    class Meta:
        db_table = "recuperacao"

# configuração
class Configuracao(models.Model):
    usuario = models.OneToOneField(User, related_name="configutacao", on_delete=models.CASCADE)
    pode_adicinar_produto = models.BooleanField(default=False)
    pode_atualizar_produto = models.BooleanField(default=False)
    pode_excluir_produto = models.BooleanField(default=False)
    pode_adicinar_fornecerdor = models.BooleanField(default=False)
    pode_atualizar_fornecerdor = models.BooleanField(default=False)
    pode_excluir_fornecedor = models.BooleanField(default=False)
    acesso_relatorios = models.BooleanField(default=False)
    acesso_configuracao_sistema = models.BooleanField(default=False)
    permissao_total = models.BooleanField(default=False)

    class Meta:
        db_table = "configuracao"