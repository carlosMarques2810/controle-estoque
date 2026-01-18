from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.conf import settings

# principal, login e controle
class Usuario(AbstractUser):
    username = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(5)])
    email = models.EmailField(max_length=225, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.username

# logs de logins
class Login(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="acessos", on_delete=models.CASCADE)
    data_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.email} - {self.data_login}"
    
    class Meta:
        db_table = "logins"

# recuperação de acesso.
class Recuperacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="recuperacao", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiracao = models.DateTimeField()

    class Meta:
        db_table = "recuperacao"

# permissões dos usuarios 
class Configuracao(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="configuracao", on_delete=models.CASCADE,)
    pode_adicionar_produto = models.BooleanField(default=False)
    pode_atualizar_produto = models.BooleanField(default=False)
    pode_excluir_produto = models.BooleanField(default=False)
    pode_adicionar_fornecerdor = models.BooleanField(default=False)
    pode_atualizar_fornecerdor = models.BooleanField(default=False)
    pode_excluir_fornecerdor = models.BooleanField(default=False)
    acesso_relatorios = models.BooleanField(default=False)
    acesso_configuracao_sistema = models.BooleanField(default=False)
    permissao_total = models.BooleanField(default=False)

    class Meta:
        db_table = "configuracoes"