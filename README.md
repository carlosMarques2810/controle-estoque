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

#### Comportamento

- **Não autenticado** → cria um novo usuário **gerente**
- **Autenticado e gerente** → cria um usuário **gerenciado por ele**
- **Autenticado e não gerente** → acesso negado

📌 Regra aplicada no método `perform_create`.

---

### ▶ Listar usuários
**GET** `/api/usuarios/`

#### Comportamento

- **Gerente** → lista somente os usuários gerenciados por ele
- **Usuário comum** → retorna apenas ele mesmo

📌 Controlado no método `get_queryset`.

---

### ▶ Detalhar usuário
**GET** `/api/usuarios/{id}/`

#### Comportamento

- **Gerente** → pode acessar usuários que ele gerencia
- **Usuário comum** → pode acessar apenas seus próprios dados

📌 Controlado por permissões personalizadas (`has_object_permission`).

---

### ▶ Atualizar usuário
**PUT / PATCH** `/api/usuarios/{id}/`

#### Comportamento

- **Gerente** → pode atualizar usuários gerenciados por ele
- **Usuário comum** → pode atualizar apenas seus próprios dados

📌 Controlado por permissões personalizadas.

---

### ▶ Remover usuário
**DELETE** `/api/usuarios/{id}/`

#### Comportamento

- **Gerente** → pode remover usuários que ele gerencia
- **Usuário comum** → pode remover apenas sua própria conta

📌 Controlado por permissões personalizadas.

---

### ▶ Histórico de logins
**GET** `/api/usuarios/{id}/logins/`

#### Comportamento

- **Apenas gerente**
- Retorna o histórico de acessos do usuário

📌 Rota criada com `@action(detail=True)`.

---

### ▶ Configuração do usuário
**GET** `/api/usuarios/{id}/configuracao/`  
**PUT / PATCH** `/api/usuarios/{id}/configuracao/`

#### Comportamento

- **Gerente** → pode visualizar e alterar as configurações de qualquer usuário
- **Usuário comum** → não possui acesso

📌 A configuração é criada automaticamente via `signal (post_save)`.

---

## 🔐 Autenticação JWT

### ▶ Login
**POST** `/api/auth/token/`

#### Entrada
```json
{
  "email": "usuario@email.com",
  "password": "senha"
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

- Todas as rotas (**exceto criação de usuário e login**) exigem autenticação **JWT**
- O controle de acesso é feito por:
  - get_queryset
  - perform_create
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
---