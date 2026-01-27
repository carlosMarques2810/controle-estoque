from rest_framework.permissions import BasePermission

class FornecedorTemPermissao(BasePermission):
    """
    Controla permissões de acesso a fornecedores.

    - Usuário comum:
        • Pode listar os fornecedores
    - Usuário com permissões administrativas:
        • Pode gerenciar fornecedores
        • Pode alterar dados de fornecedores
        • Pode apagar fonecedores
    """
    message = "Você não tem permissão para executar essa ação."

    def has_permission(self, request, view):
        user = request.user
        config = user.configuracao
        action = view.action

        if config.permissao_total:
            return True

        permissoes = {
            "create": config.pode_adicionar_fornecedor,
            "update": config.pode_atualizar_fornecedor,
            "partial_update": config.pode_atualizar_fornecedor,
            "destroy": config.pode_excluir_fornecedor,
        }

        return permissoes.get(action, True)
    
class ProdutoTemPermissao(BasePermission):
    """
    Controla permissões de acesso a fornecedores.

    - Usuário comum:
        • Pode listar os produtos
    - Usuário com permissões administrativas:
        • Pode gerenciar produtos
        • Pode alterar dados de produtos
        • Pode apagar produtos
    """
    message = "Você não tem permissão para executar essa ação."

    def has_permission(self, request, view):
        user = request.user
        config = user.configuracao
        action = view.action

        if config.permissao_total:
            return True

        permissoes = {
            "create": config.pode_adicionar_produto,
            "update": config.pode_atualizar_produto,
            "partial_update": config.pode_atualizar_produto,
            "destroy": config.pode_excluir_produto,
        }

        return permissoes.get(action, True)
