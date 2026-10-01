# SPA Backend — FastAPI + PostgreSQL

REST API для социальной сети (посты, группы, комментарии, подписки) на FastAPI с асинхронным SQLAlchemy и PostgreSQL. Аутентификация — JWT через `fastapi-users`.

## 🧱 Стек

| Компонент | Версия / описание |
|---|---|
| Python | 3.11 (в Docker) |
| FastAPI | 0.136.1 |
| SQLAlchemy | 2.0.49 (async) |
| Alembic | 1.18.4 |
| PostgreSQL | 16 (alpine) |
| asyncpg | 0.31.0 (драйвер) |
| fastapi-users | 15.0.5 |
| fastapi-pagination | 0.15.12 |
| Pydantic | 2.13.5 |
| Uvicorn | 0.46.0 |

## 🏗 Архитектура

Проект построен по слоям:

```
Request → Router → Service → Repository → SQLAlchemy → PostgreSQL
```

- **Routers** (`app/routers/`) — HTTP-слой, валидация запросов/ответов.
- **Services** (`app/services/`) — бизнес-логика.
- **Repositories** (`app/repositories/`) — работа с БД.
- **Models** (`app/models.py`) — SQLAlchemy-модели.
- **Schemas** (`app/schemas.py`) — Pydantic-схемы.
- **Core** (`app/core/`) — настройки, зависимости, исключения, auth.

## 📁 Структура проекта

```
FastApiProject/
├── alembic/
│   ├── versions/           # Миграции
│   └── env.py              # Конфигурация Alembic (async)
├── app/
│   ├── core/               # Настройки, auth, утилиты, исключения
│   ├── repositories/       # Слой доступа к данным
│   ├── routers/            # HTTP-эндпоинты
│   ├── services/           # Бизнес-логика
│   ├── database.py         # Async engine, session, Base
│   ├── main.py             # Точка входа FastAPI
│   ├── models.py           # SQLAlchemy-модели
│   └── schemas.py          # Pydantic-схемы
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── .env
```

## 🚀 Быстрый старт (Docker)

### 1. Создайте общую сеть (один раз)

Backend и frontend должны быть в одной сети, чтобы nginx мог проксировать на `ssa_backend`:

```bash
docker network create ssa_net
```

### 2. Подготовьте `.env`

Создайте файл `.env`.
Скопируйте `.envexample` → `.env`, заполните значения.

### 3. Поднимите БД

```bash
docker compose up -d db
```

Дождитесь статуса `(healthy)`:
```bash
docker compose ps
```

### 4. Соберите и запустите backend

```bash
docker compose build --no-cache backend
docker compose up -d backend
docker compose logs -f backend
```

При старте `entrypoint.sh`:
1. Ждёт БД (до 10 попыток, 2 сек интервал).
2. Применяет миграции: `alembic upgrade head`.
3. Запускает `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

### 5. Проверьте

- Swagger UI: <http://127.0.0.1:8000/docs>
- OpenAPI: <http://127.0.0.1:8000/openapi.json>
- Эндпоинт постов: <http://127.0.0.1:8000/posts/>

> ⚠️ На Windows используйте `127.0.0.1`, а не `localhost` — Docker Desktop часто ломает IPv6-проброс.

## 🛠 Локальная разработка (без Docker)

### 1. Установите Python 3.11+ и поднимите Postgres

Можно использовать только контейнер с БД:
```bash
docker compose up -d db
```
Postgres будет доступен на `localhost:5432` (проброшен в `docker-compose.yml`).

### 2. Создайте виртуальное окружение

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/macOS
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Задайте `DATABASE_URL`

```bash
# Windows PowerShell
$env:DATABASE_URL = "postgresql+asyncpg://your_user:your_password@localhost:5432/your_db"

# Linux/macOS
export DATABASE_URL="postgresql+asyncpg://your_user:your_password@localhost:5432/your_db"
```

### 5. Примените миграции и запустите

```bash
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🗄 Миграции (Alembic)

Alembic настроен на **async**-режим (`alembic/env.py` использует `async_engine_from_config` и `asyncpg`).

### Создать новую миграцию

После изменения моделей в `app/models.py`:

```bash
# Убедитесь, что БД запущена
docker compose up -d db

# Задайте URL для локального запуска
$env:DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"

# Сгенерируйте миграцию
alembic revision --autogenerate -m "add field X to posts"

# Проверьте файл в alembic/versions/ глазами

# Уберите переменную
Remove-Item Env:\DATABASE_URL
```

### Применить миграции

```bash
# Локально
alembic upgrade head

# Через контейнер
docker compose run --rm backend alembic upgrade head
```

### Откатить последнюю миграцию

```bash
alembic downgrade -1
```

### Посмотреть историю

```bash
alembic history
alembic current
```

> 💡 **Важно:** миграции должны быть в git. В `entrypoint.sh` они применяются автоматически при старте контейнера.

## 📊 Модели данных

| Таблица | Назначение | Ключевые поля |
|---|---|---|
| `users` | Пользователи (fastapi-users) | `id`, `email`, `username`, `hashed_password`, `is_active`, `is_superuser`, `is_verified` |
| `groups` | Группы/сообщества | `id`, `title`, `slug`, `description` |
| `posts` | Посты | `id`, `text`, `pub_date`, `author_id`, `group_id`, `image` |
| `comments` | Комментарии | `id`, `text`, `pub_date`, `post_id`, `author_id` |
| `follows` | Подписки | `id`, `user_id`, `author_id` |

Связи:
- `User` → `Post` (1:N), `User` → `Comment` (1:N)
- `Group` → `Post` (1:N)
- `Post` → `Comment` (1:N)
- `User` ↔ `User` через `Follow` (подписки)

## 🔌 API

Базовый URL: `http://127.0.0.1:8000`

### Auth (`/auth`)

| Метод | Путь | Описание |
|---|---|---|
| POST | `/auth/jwt/login` | Логин, выдаёт JWT |
| POST | `/auth/jwt/logout` | Выход (требует токен) |
| POST | `/auth/register` | Регистрация |
| POST | `/auth/forgot-password` | Запрос сброса пароля |
| POST | `/auth/reset-password` | Сброс пароля по токену |

### Users (`/users`)

| Метод | Путь | Описание |
|---|---|---|
| GET | `/users/me` | Текущий пользователь |
| PATCH | `/users/me` | Обновить себя |
| DELETE | `/users/me` | Удалить себя |
| GET | `/users/{id}` | Получить пользователя (superuser) |
| PATCH | `/users/{id}` | Обновить (superuser) |
| DELETE | `/users/{id}` | Удалить (superuser) |

### Posts (`/posts`)

| Метод | Путь | Описание |
|---|---|---|
| GET | `/posts/` | Лента постов (пагинация, поиск `?q=`) |
| POST | `/posts/` | Создать пост |
| GET | `/posts/{post_id}` | Детали поста |
| PATCH | `/posts/{post_id}/` | Редактировать пост |
| DELETE | `/posts/{post_id}/` | Удалить пост |
| POST | `/posts/{post_id}/comments/` | Добавить комментарий |

### Прочее

| Метод | Путь | Описание |
|---|---|---|
| GET | `/follow/` | Лента подписок |
| GET | `/profile/me` | Свой профиль |
| GET | `/profile/{username}` | Профиль пользователя |
| POST | `/profile/{username}/follow/` | Подписаться |
| DELETE | `/profile/{username}/follow/` | Отписаться |
| GET | `/groups/` | Список групп |
| POST | `/groups/` | Создать группу |
| GET | `/groups/{slug}/` | Посты группы |

> 📄 Полная спецификация — Swagger: `/docs`, ReDoc: `/redoc`.

### Аутентификация

Все защищённые эндпоинты требуют заголовок:

```
Authorization: Bearer <access_token>
```

Токен получается через `POST /auth/jwt/login` (form-data: `username`, `password`).

## 🐳 Docker-сервисы

### `db`

- **Образ:** `postgres:16-alpine`
- **Порт:** `5432:5432` (для отладки через DBeaver/pgAdmin)
- **Volume:** `pg_data` — данные сохраняются между перезапусками
- **Healthcheck:** `pg_isready`

### `backend`

- **Образ:** собран из `Dockerfile`
- **Порт:** `8000:8000`
- **Зависит от:** `db` (`service_healthy`)
- **Healthcheck:** `curl -f http://localhost:8000/posts/`
- **Restart:** `unless-stopped`

## 🔒 Безопасность

- **`.env`** — в `.gitignore`. Есть `.env.example` с плейсхолдерами.
- **Пароль Postgres** — без спецсимволов (`@`, `:`, `/`, `#`, `%`), иначе URL `DATABASE_URL` сломается. Генерируйте через `secrets.token_urlsafe`.
- **Порт 5432** — в проде уберите проброс (`ports:`) у `db` или привяжите к `127.0.0.1:5432:5432`.
- **CORS** — если фронт на другом origin, добавьте `CORSMiddleware` с явным списком origins.

## 🧪 Полезные команды

```bash
# Логи backend в реальном времени
docker compose logs -f backend

# Зайти в контейнер backend
docker compose exec backend sh

# Открыть psql
docker exec -it ssa_db psql -U <user> -d <db>

# Список таблиц
docker exec -it ssa_db psql -U <user> -d <db> -c "\dt"

# Проверить статус контейнеров
docker compose ps

# Пересобрать backend без кеша
docker compose build --no-cache backend

# Перезапустить backend
docker compose restart backend

# Полная остановка с удалением volume (данные БД удалятся!)
docker compose down -v
```

## 🐛 Troubleshooting

**`Connection refused` к Postgres**

- Проверьте `docker compose ps` — `ssa_db` должен быть `(healthy)`.
- Проверьте `netstat -ano | Select-String ":5432"` — порт не занят другим Postgres.
- Volume мог быть инициализирован со старыми `POSTGRES_*`. Удалите: `docker compose down -v` и поднимите заново.

**`relation "..." does not exist`**

- Миграции не применены. `docker compose run --rm backend alembic upgrade head`.
- Проверьте `alembic/versions/` — там должны быть файлы миграций.

**`ModuleNotFoundError: asyncpg.protocol.protocol`** (Python 3.14)

- Используйте Python 3.11–3.13. Либо обновите `asyncpg` до 0.31.0+ — там есть wheels для 3.14.

**`Connection reset` при запросе с хоста**

- На Windows используйте `127.0.0.1` вместо `localhost` (проблема IPv6 + Docker Desktop).
- Проверьте, что порт не занят другим процессом: `netstat -ano | Select-String ":8000"`.

---
