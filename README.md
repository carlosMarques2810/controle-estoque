# Django - Controle de estoque

🚧 Projeto em desenvolvimento

Backend de controle de estoque desenvolvido com **Django**, utilizando **PostgreSQL em Docker**.

## 🛠 Tecnologias
* **Linguagem & Core:**
    * ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    * ![POO](https://img.shields.io/badge/Programação%20Orientada%20a%20Objetos-000000?style=for-the-badge&logo=code&logoColor=white)

* **Framework & Backend:**
    * ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
    * ![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-A30000?style=for-the-badge&logo=django&logoColor=white)
    * ![JWT](https://img.shields.io/badge/JWT%20Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

* **Autenticação & Segurança:**
    * ![SimpleJWT](https://img.shields.io/badge/SimpleJWT-4B0082?style=for-the-badge)
    * ![Permissions](https://img.shields.io/badge/Permissões%20Customizadas-2A9D8F?style=for-the-badge)
    * ![Signals](https://img.shields.io/badge/Django%20Signals-1F618D?style=for-the-badge)

* **Configuração & Ambiente:**
    * ![Python Decouple](https://img.shields.io/badge/python--decouple-000000?style=for-the-badge)
    * ![Env Vars](https://img.shields.io/badge/Variáveis%20de%20Ambiente-264653?style=for-the-badge)

* **Banco de Dados:**
    * ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
    * ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

* **Infraestrutura & DevOps:**
    * ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
    * ![Docker Compose](https://img.shields.io/badge/Docker%20Compose-0db7ed?style=for-the-badge&logo=docker&logoColor=white)

* **Testes & Qualidade:**
    * ![Django Tests](https://img.shields.io/badge/Testes%20com%20Django-0C4B33?style=for-the-badge)
    * ![DRF APIClient](https://img.shields.io/badge/DRF%20APIClient-8E44AD?style=for-the-badge)

* **Ferramentas de Desenvolvimento:**
    * ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
    * ![GitHub](https://img.shields.io/badge/GitHub-121011?style=for-the-badge&logo=github&logoColor=white)
---

## 🎯 Objetivo
Este projeto tem como objetivo o desenvolvimento de um sistema, back-end, de controle de estoque, referente a uma parte do **Projeto Integrador III** do curso de Análise e Desenvolvimento de Sistemas, aplicando conceitos de modelagem de dados e boas práticas de desenvolvimento utilizando Django e PostgreSQL.


## ⚙️ Banco de Dados
O PostgreSQL é executado em um container Docker, enquanto o Django roda localmente.

### 🗄️ Banco de Dados

Por padrão, ao clonar e rodar o projeto localmente, é utilizado o **SQLite**, pois ele já vem integrado ao Django e não exige nenhuma configuração adicional.

- O arquivo do banco é criado automaticamente (`db.sqlite3`)
- Ideal para testes, desenvolvimento local e avaliação do projeto

#### 🐳 PostgreSQL com Docker (opcional)

Durante o desenvolvimento, o projeto também pode ser utilizado com **PostgreSQL rodando em Docker**.

⚠️ **Observação:**  
A configuração com Docker + PostgreSQL **não é obrigatória** para rodar o projeto após o clone.  
Caso o desenvolvedor deseje utilizar PostgreSQL, será necessário ajustar as variáveis de ambiente e o `settings.py`.

👉 Para avaliação rápida do projeto, **recomenda-se usar SQLite**.

## 🔐 Configurações
As variáveis de ambiente são gerenciadas via `.env` (não versionado).

### ⚙️ Configuração opcional com `.env`

Este projeto **não exige obrigatoriamente** a criação de um arquivo `.env` para rodar em ambiente local.

O arquivo `.env` serve apenas para **personalizar o ambiente de testes e desenvolvimento**.  
Caso não seja criado, o sistema utilizará **valores padrão**.

```env
# Ativa o banco de dados de testes (SQLite)
DB_TESTE=True

# Ativa o modo debug
DEBUG=True

# (Opcional) Credenciais do superusuário
# Se não forem informadas, valores padrão serão utilizados
SUPERUSER_USERNAME=userteste
SUPERUSER_EMAIL=test@email.com
SUPERUSER_PASSWORD=test1234
```
---

## 🚀 Instalação e rodar localmente.

> Requisitos: Python 3.10+ e pip

### 1. Clone o repositório
```bash
git clone https://github.com/carlosMarques2810/controle-estoque.git
cd controle-estoque  
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows 
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Aplique as migrações
```bash
python manage.py makemigrations
python manage.py migrate   
```

#### 4.1. Usuário Root (pós migrações)

> Um superusuário é criado automaticamente após as migrações.
>
> **SUPERUSER** — possui todas as permissões do sistema  
> **EMAIL:** informado no `.env` (opcional) ou **valor padrão**  
> **SENHA:** informada no `.env` (opcional) ou **valor padrão**

### 5. Inicie o servidor
```bash
python manage.py runserver
```
---

## 🧪 Interface Web do Django REST Framework

Este projeto utiliza a **interface web interativa do Django REST Framework**, que facilita:

- Testar todas as rotas da API diretamente pelo navegador
- Visualizar claramente os **dados de entrada (request)** e **dados de saída (response)**
- Entender quais campos são obrigatórios ou opcionais
- Ver mensagens de erro de validação no padrão DRF

📌 A interface é automaticamente habilitada em ambiente de desenvolvimento.

Após iniciar o servidor, acesse:

http://127.0.0.1:8000/api/

Na interface do DRF:
- Os formulários exibem os campos esperados pela rota
- Os erros de validação aparecem associados aos campos inválidos
- Tokens JWT podem ser enviados no header `Authorization`

Essa interface é especialmente útil para:
- Testes manuais
- Aprendizado da API
- Debug durante o desenvolvimento
---

## 🚀 Rotas da API

### ▶ Criar usuário
**POST** `/api/usuarios/`

### Entrada
```json
{
  "nome_do_usuario": "Carlos Silva",
  "email": "carlos@email.com",
  "senha": "senha123",
  "confirmacao_senha": "senha123"
}
```

### Saída
```json
{
  "id": 1,
  "nome_do_usuario": "Carlos Silva",
  "email": "carlos@email.com"
}
```

#### Comportamento

- **Superusuário** → cria um usuário
- **Usuário comun** → acesso negado

---

### ▶ Listar usuários
**GET** `/api/usuarios/`

### Saída
```json
[
  {
    "id": 1,
    "nome_do_usuario": "Carlos Silva",
    "email": "carlos@email.com"
  },
  {
    "id": 2,
    "nome_do_usuario": "Maria Souza",
    "email": "maria@email.com"
  }
]
```

#### Comportamento
- **Superusuário** → lista todos os usuários
- **Usuário comum** → retorna apenas ele mesmo

📌 Controlado no método `get_queryset`.

---

### ▶ Detalhar usuário
**GET** `/api/usuarios/{id}/`

### Saída
```json
{
  "id": 1,
  "nome_do_usuario": "Carlos Silva",
  "email": "carlos@email.com"
}
```

#### Comportamento

- **Superusuário** → pode acessar usuários
- **Usuário comum** → pode acessar apenas seus próprios dados

📌 Controlado por permissões personalizadas (`has_object_permission`).

---

### ▶ Atualizar usuário
**PUT / PATCH** `/api/usuarios/{id}/`

### Entrada
```json
{
  "nome_do_usuario": "Carlos Silva",
  "email": "carlos@email.com"
}
```

### Saída
```json
{
  "id": 1,
  "nome_do_usuario": "Carlos Silva",
  "email": "carlos@email.com"
}
```

#### Comportamento

- **Superusuário** → pode atualizar usuários
- **Usuário comum** → atuliza os próprios dados

📌 Controlado por permissões personalizadas.

---

### ▶ Remover usuário
**DELETE** `/api/usuarios/{id}/`

#### Comportamento

- **Superusuário** → pode remover usuários
- **Usuário comum** → acesso negado

📌 Controlado por permissões personalizadas.

---

### ▶ Histórico de logins
**GET** `/api/usuarios/{id}/logins-logs/`

### Saída
```json
[
  {
    "id": 1,
    "usuario": 1,
    "login_data": "2026-0115T14:32:10Z"
  },
  {
    "id": 2,
    "usuario": 1,
    "login_data": "2026-0117T09:08:44Z"
  }
]
```

#### Comportamento

- **Superusuário**
- Retorna o histórico de acessos do usuário

📌 Rota criada com `@action(detail=True)`.

---

### ▶ Configuração do usuário
**GET** `/api/usuarios/{id}/premissoes/`  

### Saída 
```json
{
  "usuario": 1,
  "pode_adicionar_produto": true,
  "pode_atualizar_produto": false,
  "pode_excluir_produto": false,
  "pode_adicionar_fornecedor": true,
  "pode_atualizar_fornecedor": false,
  "pode_excluir_fornecedor": false,
  "acesso_relatorios": true,
  "acesso_configuracao_sistema": false,
  "permissao_total": false
}
```

**PUT / PATCH** `/api/usuarios/{id}/permissoes/`

### Entrada
```json
{
  "pode_adicionar_produto": true,
  "pode_excluir_produto": true,
  "acesso_relatorios": true
}
```

### Saída
```json
{
  "usuario": 1,
  "pode_adicionar_produto": true,
  "pode_atualizar_produto": false,
  "pode_excluir_produto": true,
  "pode_adicionar_fornecedor": true,
  "pode_atualizar_fornecedor": false,
  "pode_excluir_fornecedor": false,
  "acesso_relatorios": true,
  "acesso_configuracao_sistema": false,
  "permissao_total": false
}
```

#### Comportamento

- **Superusuário** → pode visualizar e alterar as configurações de qualquer usuário
- **Usuário comum** → só pode visualizar as suas configurações

📌 A configuração é criada automaticamente via `signal (post_save)`.

---

## 🔐 Autenticação JWT

### ▶ Login
**POST** `/api/auth/token/`

#### Entrada
```json
{
  "email": "usuario@email.com",
  "password": "senha1234"
}
```

### Saída
```json
{
  "refresh": "token_refresh",
  "access": "token_access"
}
```
----
## ▶ Refresh do token
**POST** `/api/auth/refresh/`

#### Entrada
```json
{
  "refresh": "token_refresh"
}
```

### Saída
```json
{
  "access": "novo_token_access"
}

```
---

## 🛡️ Observações de segurança

- Todas as rotas exigem autenticação **JWT**
- O controle de acesso é feito por:
  - get_queryset
  - permissões personalizadas (BasePermission)
- As rotas extras (**logins** e **configuracao**) são actions do ModelViewSet
---

## ❗ Padrão de retorno de erros

A API segue o padrão do **Django REST Framework (DRF)**.

- Erros gerais vêm no campo **detail**
- Erros de validação vêm por **campo**, com a mensagem do erro
---

### Exemplo - de erros gerais

- **401 Unauthorized**
  - Usuário não autenticado
  ```json
  { "detail": "As credenciais de autenticação não foram fornecidas." }

  ```

- **403 Forbidden**  
   - Usuário autenticado, mas sem permissão  
   ```json
   { "detail": "Você não tem permissão para executar essa ação." }
   ```

- **404 Not Found**  
   - Recurso não encontrado
   ```json
   { "detail": "Não encontrado." }
   ```

- **400 Bad Request**  
   - Erro de validação geral
   ```json
   { "detail": "Dados inválidos." }
   ```   


- **500 Internal Server Error**  
   - Erro interno inesperado
   ```json
   { "detail": "Erro interno do servidor." }
   ```   
---
### Exemplo — erro de validação
```json
{
  "email": [
    "Este campo é obrigatório."
  ],
  "senha": [
    "Este campo não pode ser em branco."
  ]
}
```

### Tratamento de erros no Front-end

O front-end deve tratar erros com base no **status HTTP** retornado pela API.

As mensagens retornadas no corpo da resposta (`detail`) não devem ser usadas como regra de negócio,
servindo apenas como apoio para debug ou exibição opcional.

Erros de validação (`400`) retornam mensagens por campo e podem ser utilizados para feedback ao usuário.
---
