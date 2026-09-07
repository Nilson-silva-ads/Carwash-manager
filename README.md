# Carwash Manager

Sistema web para gerenciamento de atendimentos em um posto de lavagem de veículos. A aplicação possui autenticação de funcionários, controle de permissões por perfil, cadastro de veículos e atendimentos, relatórios e interface responsiva com suporte a PWA.

## Visão geral

O Carwash Manager foi estruturado para centralizar a operação diária do lava-jato, permitindo registrar os serviços realizados, consultar o histórico por placa ou período e administrar os usuários e tipos de serviço disponíveis.

O projeto é composto por uma API em FastAPI e uma aplicação frontend em React/Vite. O backend utiliza PostgreSQL como banco de dados, com SQLAlchemy para persistência e Alembic para versionamento do schema.

## Funcionalidades

- Login de funcionários com autenticação baseada em token JWT.
- Perfis de acesso para administrador (ADM) e funcionário.
- Cadastro e consulta de veículos e atendimentos.
- Atendimento com múltiplos serviços.
- Edição de atendimento restrita ao perfil ADM.
- Consulta de atendimentos por placa e por período.
- Gerenciamento de funcionários.
- Gerenciamento de tipos de serviço.
- Relatórios operacionais, incluindo veículos cadastrados por funcionário durante o mês.
- Dashboard e navegação protegida após o login.
- Interface responsiva para uso em celular e computador.
- PWA instalável e funcional em dispositivos móveis.

## Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT, com `python-jose`
- Uvicorn

### Frontend

- React 18
- TypeScript
- Vite
- React Router
- `vite-plugin-pwa`
- Lucide React

### Infraestrutura

- Supabase/PostgreSQL para o banco de dados.
- Render para hospedagem da API.
- Vercel para hospedagem do frontend.

## Arquitetura

O projeto segue uma arquitetura em camadas, separando responsabilidades entre entrada HTTP, regras de negócio e persistência:

```text
Cliente/PWA
    |
    v
Frontend React/Vite
    |
    v
API FastAPI
    |
    +-- Routes       -> endpoints HTTP
    +-- Schemas      -> validação e serialização
    +-- Services     -> regras de negócio
    +-- Repositories -> acesso aos dados
    +-- Models       -> entidades SQLAlchemy
    |
    v
PostgreSQL / Supabase
```

## Estrutura do projeto

```text
.
├── app/
│   ├── core/           # autenticação, configuração, exceções e rotas
│   ├── database/       # sessão e base do banco
│   ├── dependencies/   # dependências das rotas
│   ├── models/         # modelos SQLAlchemy
│   ├── repositories/   # persistência
│   ├── routes/          # endpoints da API
│   ├── schemas/         # schemas Pydantic
│   ├── seeds/           # dados iniciais de tipos de serviço
│   └── services/        # regras de negócio
├── alembic/
│   └── versions/        # migrations do banco
├── frontend/
│   ├── public/          # ícones, imagens e recursos do PWA
│   └── src/
│       ├── components/  # componentes reutilizáveis
│       ├── pages/       # telas da aplicação
│       ├── api.ts       # comunicação com a API
│       └── auth.tsx     # contexto de autenticação
├── tests/               # diretório reservado para testes
├── create_admin.py      # criação do usuário administrador
├── requirements.txt
├── alembic.ini
├── Procfile
└── .env.example
```

## Execução local

### Pré-requisitos

- Python compatível com a versão definida em `runtime.txt`.
- Node.js e npm.
- Uma instância PostgreSQL local ou um banco PostgreSQL no Supabase.

### Backend

Na raiz do projeto, crie e ative um ambiente virtual e instale as dependências:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha os valores do ambiente local. Depois, aplique as migrations e inicie a API:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

A API ficará disponível, por padrão, em `http://127.0.0.1:8000`. A documentação interativa do FastAPI pode ser acessada em `/docs`.

Para criar o administrador inicial, use o script existente após configurar o banco e as variáveis de ambiente:

```bash
python create_admin.py
```

### Frontend

Em outro terminal:

```bash
cd frontend
npm install
```

Crie `frontend/.env` a partir de `frontend/.env.example` e configure a URL da API:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

Para gerar a versão de produção:

```bash
npm run build
npm run preview
```

## Variáveis de ambiente

Nunca versionar valores reais ou secrets. Os arquivos `.env.example` documentam as variáveis esperadas.

### Backend — `.env`

| Variável | Finalidade |
| --- | --- |
| `DATABASE_URL` | URL de conexão com o PostgreSQL/Supabase |
| `SECRET_KEY` | Chave usada para assinar tokens; deve ter pelo menos 32 caracteres |
| `JWT_ALGORITHM` | Algoritmo JWT, atualmente configurado como `HS256` por padrão |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token |
| `CORS_ORIGINS` | Origens autorizadas para acessar a API |
| `ADMIN_NAME` | Nome do administrador inicial |
| `ADMIN_USERNAME` | Usuário do administrador inicial |
| `ADMIN_PASSWORD` | Senha do administrador inicial |

### Frontend — `frontend/.env`

| Variável | Finalidade |
| --- | --- |
| `VITE_API_URL` | URL base da API do backend |

## Autenticação e permissões

O login é realizado pelo endpoint de funcionários e retorna um token de acesso. O frontend armazena o token para manter a sessão e protege as rotas internas da aplicação.

O perfil ADM possui permissão para editar atendimentos e gerenciar funcionários e tipos de serviço. O perfil funcionário pode utilizar as operações permitidas ao seu nível de acesso, respeitando as regras implementadas na API.

Em produção, configure `SECRET_KEY`, senhas e credenciais específicas do ambiente. Não utilize os valores de exemplo.

## Banco de dados e migrations

As entidades são mapeadas com SQLAlchemy. As alterações estruturais do banco são controladas pelo Alembic e ficam em `alembic/versions/`.

Comandos principais:

```bash
alembic upgrade head       # aplica todas as migrations
alembic current             # consulta a versão atual
alembic downgrade -1       # retorna uma migration, quando necessário
```

O banco pode ser um PostgreSQL local ou uma instância PostgreSQL fornecida pelo Supabase, desde que `DATABASE_URL` esteja corretamente configurada.

## Deploy

### API no Render

O arquivo `Procfile` define o processo web da API:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port $port
```

No Render, configure as variáveis de ambiente do backend e execute as migrations no banco de produção antes de disponibilizar a aplicação.

### Frontend na Vercel

Configure o projeto apontando para a pasta `frontend`, use `npm run build` como comando de build e defina `VITE_API_URL` com a URL pública da API no Render.

Também inclua a URL pública do frontend em `CORS_ORIGINS` no backend.

## PWA e uso em celular

O frontend possui configuração de PWA por meio do `vite-plugin-pwa`, além de manifest e ícones em `frontend/public/`. A aplicação foi preparada para uso responsivo em celular e computador e pode ser instalada pelo navegador quando o ambiente publicado estiver usando HTTPS.

## Testes e validação

O build do frontend pode ser validado com:

```bash
cd frontend
npm run build
```

No estado atual do repositório, o diretório `tests/` não contém testes automatizados implementados. A validação da versão deve incluir, no mínimo, login com os dois perfis, cadastro de atendimento com múltiplos serviços, restrições de edição, consultas, cadastros administrativos, relatórios, migrations e instalação/uso do PWA em um dispositivo móvel.

## Status da versão 1.0

**Versão:** `1.0.0`

A versão 1.0.0 reúne o fluxo principal de autenticação, operação de atendimentos, administração de funcionários e serviços, consultas, relatórios e distribuição separada do backend e frontend. O projeto está preparado para execução local e deploy em Render, Vercel e PostgreSQL/Supabase.

Antes de considerar uma publicação definitiva, valide as variáveis de produção, as migrations no banco remoto, o CORS, o fluxo completo dos perfis e o build do frontend.
