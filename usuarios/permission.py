from rest_framework.permissions import BasePermission

class UsuarioTemPermissao(BasePermission):
    """
    Controla permissões de acesso a usuários e configurações.

    - Usuário comum:
        • Pode ver apenas seus próprios dados
        • Pode ver sua própria configuração
    - Usuário com permissões administrativas:
        • Pode gerenciar usuários
        • Pode alterar configurações
    """
    message = "Você não tem permissão para executar essa ação."

    def has_permission(self, request, view):
        user = request.user
        if view.action in ["create", "update", "partial_update", "destroy"]:
            return user.configuracao.permissao_total or user.configuracao.acesso_configuracao_sistema
        
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        if action in ["configuracao", "retrieve"] and request.method == "GET":
            return user.id == obj.id or user.configuracao.permissao_total or user.configuracao.acesso_configuracao_sistema

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return user.configuracao.permissao_total or user.configuracao.acesso_configuracao_sistema

        return False
