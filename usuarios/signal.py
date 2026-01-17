from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Configuracao

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
        if instance.is_gerente:
            configuracao = Configuracao(usuario=instance, **configuracoes)

        configuracao.save()