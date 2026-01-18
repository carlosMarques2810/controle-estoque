from rest_framework.permissions import BasePermission

class ApenasSuperuser(BasePermission):
    """
    Regras:
    - Superuser:
        - Pode ver e alterar usuários que ele gerencia
        - Pode acessar configuracao e logins
    - Usuário comum:
        - Pode ver e editar apenas a si mesmo
        - NÃO acessa configuracao nem logins
    """
    message = "Você não tem permissão para executar essa ação."

    def has_permission(self, request, view):
        # actions que exigem login
        if view.action in ["retrieve", "update", "partial_update", "destroy", "configuracao", "logins"]:
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        action = view.action

        if action in ["configuracao", "logins", "destroy"]:
            return user.is_superuser

        if action in ["retrieve", "update", "partial_update"]:
            if user.is_superuser:
                return True

            return obj.id == user.id

        return False
