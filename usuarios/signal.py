from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Configuracao
from decouple import config

Usuario = get_user_model()

@receiver(post_migrate)
def criar_superuser(sender, **kwargs):
    dados = {
        "username": config("SUPERUSER_USERNAME"),
        "email": config("SUPERUSER_EMAIL"),
        "password": config("SUPERUSER_PASSWORD")
    }

    if not Usuario.objects.filter(is_superuser=True).exists():
        Usuario.objects.create_superuser(**dados)

@receiver(post_save, sender=Usuario)
def criar_configuracao_usuario(sender, instance, created, **kwargs):
    if created:
        configuracoes = {
            "pode_adicionar_produto": True,
            "pode_atualizar_produto": True, 
            "pode_excluir_produto": True, 
            "pode_adicionar_fornecerdor": True,
            "pode_atualizar_fornecerdor": True,
            "pode_excluir_fornecerdor": True,
            "acesso_relatorios": True,
            "acesso_configuracao_sistema": True,
            "permissao_total": True
        }
        
        configuracao = Configuracao(usuario=instance)
        if instance.is_superuser:
            configuracao = Configuracao(usuario=instance, **configuracoes)

        configuracao.save()