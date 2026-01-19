from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Configuracao
from decouple import config

Usuario = get_user_model()

@receiver(post_migrate)
def criar_superuser(sender, **kwargs):
    if sender.name != "usuarios": return

    dados = {
        "username": config("SUPERUSER_USERNAME", default="userteste"),   
        "email": config("SUPERUSER_EMAIL", default="test@email.com"),
        "password": config("SUPERUSER_PASSWORD", default="test1234")
    }

    if not Usuario.objects.filter(is_superuser=True).exists():
        Usuario.objects.create_superuser(**dados)

@receiver(post_save, sender=Usuario)
def criar_configuracao_usuario(sender, instance, created, **kwargs):
    if created:
        configuracao = Configuracao(usuario=instance, permissao_total=instance.is_superuser)
        configuracao.save()