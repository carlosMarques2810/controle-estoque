from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Login, Configuracao, Recuperacao

Usuario = get_user_model()

# Controla os dados referentes ao usuário
class UsuarioSerializer(serializers.ModelSerializer):
    nome_do_usuario = serializers.CharField(source='username', label="Nome do usuário")
    senha = serializers.CharField(source="password", label="Senha", style={"input_type": "password"})
    confirmar_senha = serializers.CharField(write_only=True, label="Comfirmar senha", style={"input_type": "password"})

    class Meta:
        model = Usuario
        fields = ["id", "nome_do_usuario", "email", "senha", "confirmar_senha"]
        extra_kwargs = {
            'senha': {'write_only': True}, 
            'gerente': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmar_senha']:
            raise serializers.ValidationError(
                {"confirmar_senha": "As senhas não conferem."}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("confirmar_senha")
        usuario = Usuario.objects.create_user(**validated_data)
        return usuario

# Login, token e histórico
class LoginSerilaizer(TokenObtainPairSerializer): 
    def validate(self, attrs):
        dados = super().validate(attrs)
        Login.objects.create(usuario=self.user)
        return dados

# Pemissões dos usuários
class ConfiguracaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Configuracao
        fields = [
            "usuario",  
            "pode_adicionar_produto",
            "pode_atualizar_produto", 
            "pode_excluir_produto", 
            "pode_adicionar_fornecerdor",
            "pode_atualizar_fornecerdor",
            "pode_excluir_fornecerdor",
            "acesso_relatorios",
            "acesso_configuracao_sistema",
            "permissao_total"
        ]
    
class RecuperacaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    class Meta:
        model = Recuperacao
        fields = ["usuario", "token", "expiracao"]

class LogsAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        filds = ["data_login"]