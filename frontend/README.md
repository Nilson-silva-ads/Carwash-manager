# Carwash Manager — Frontend

Frontend React + Vite + TypeScript para o Carwash Manager.

## Requisitos

- Node.js 20+
- Backend FastAPI executando

## Instalação

```bash
npm install
```

Copie `.env.example` para `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Depois:

```bash
npm run dev
```

Abra a URL mostrada pelo Vite.

## Observação sobre autenticação

O frontend usa `POST /auth/login` com `application/x-www-form-urlencoded`, compatível com o fluxo OAuth2PasswordRequestForm normalmente usado pelo FastAPI.

O token retornado em `access_token` é enviado como:

```text
Authorization: Bearer <token>
```

## Endpoints utilizados

- `POST /auth/login`
- `GET /employees`
- `POST /employees`
- `PATCH /employees/{id}/activate`
- `PATCH /employees/{id}/deactivate`
- `GET /service-types`
- `POST /service-types`
- `PATCH /service-types/{id}/activate`
- `PATCH /service-types/{id}/deactivate`
- `POST /service-orders`
- `GET /service-orders`
- `GET /reports/service-orders`
- `GET /reports/monthly`

Se a sua API usar outra rota para descobrir o funcionário autenticado, ajuste apenas `src/auth.tsx`.
