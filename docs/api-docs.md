## 📚 Полная документация API

### 1. Регистрация пользователя

**Endpoint:** `POST /api/auth/register`

**Описание:** Создание нового аккаунта в системе.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-02-19T10:30:00Z",
  "updated_at": null
}
```

**Состояние взаимодействия:**

```mermaid
sequenceDiagram
    participant Client as Client (Browser)
    participant API as FastAPI App
    participant UserService as User Service
    participant DB as PostgreSQL

    Client->>API: POST /api/auth/register {email, username, password}
    API->>UserService: validate email uniqueness
    UserService->>DB: SELECT * FROM users WHERE email = ?
    DB-->>UserService: empty result
    API->>UserService: validate username uniqueness
    UserService->>DB: SELECT * FROM users WHERE username = ?
    DB-->>UserService: empty result
    API->>UserService: hash password & create user
    UserService->>DB: INSERT INTO users (email, username, password_hash, is_active, created_at)
    DB-->>UserService: user created with id=1
    UserService-->>API: UserResponse object
    API-->>Client: 201 {id, email, username, is_active, is_verified, created_at}
```

**Возможные ошибки:**
- `400 Bad Request` — Email уже зарегистрирован
- `400 Bad Request` — Username уже существует
- `400 Bad Request` — Пароль менее 8 символов

---

### 2. Вход в систему (Login)

**Endpoint:** `POST /api/auth/login`

**Описание:** Аутентификация пользователя и получение JWT токена.

**Request Body:**
```json
{
  "login": "user@example.com",
  "password": "SecurePassword123!",
  "remember_me": true
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

**Состояние взаимодействия:**

```mermaid
sequenceDiagram
    participant Client as Client (Browser)
    participant API as FastAPI App
    participant UserService as User Service
    participant Security as Security Module
    participant DB as PostgreSQL

    Client->>API: POST /api/auth/login {login, password, remember_me}
    API->>UserService: get_by_login(login)
    UserService->>DB: SELECT * FROM users WHERE email = ? OR username = ?
    DB-->>UserService: user data
    API->>Security: verify_password(input_password, hash_from_db)
    Security-->>API: true/false
    alt Password Correct
        API->>Security: create_user_access_token(user_id, remember_me_expiry)
        Security-->>API: JWT token string
        API-->>Client: 200 {access_token, token_type: "Bearer"}
    else Password Incorrect
        API-->>Client: 403 Forbidden {detail: "Неверный пароль"}
    else User Not Found
        API-->>Client: 404 Not Found {detail: "Нет пользователя"}
    end
```

**Возможные ошибки:**
- `404 Not Found` — Пользователь не найден
- `403 Forbidden` — Неверный пароль

---

### 3. Получение профиля (Get Current User)

**Endpoint:** `GET /api/auth/me`

**Описание:** Получение информации о текущем авторизованном пользователе.

**Headers:**
```
Authorization: Bearer <ACCESS_TOKEN>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-02-19T10:30:00Z",
  "updated_at": "2026-02-19T11:00:00Z"
}
```

**Состояние взаимодействия:**

```mermaid
sequenceDiagram
    participant Client as Client (Browser)
    participant API as FastAPI App
    participant Security as Security Module
    participant UserService as User Service
    participant DB as PostgreSQL

    Client->>API: GET /api/auth/me<br/>Headers: Authorization: Bearer <token>
    API->>Security: validate JWT token
    alt Token Valid
        Security->>Security: decode token → extract user_id
        Security-->>API: user_id = 1
        API->>UserService: get_by_id(user_id)
        UserService->>DB: SELECT * FROM users WHERE id = ?
        DB-->>UserService: user data
        UserService-->>API: User object
        API-->>Client: 200 {user data}
    else Token Invalid
        API-->>Client: 401 Unauthorized {detail: "Invalid token"}
    else Token Expired
        API-->>Client: 401 Unauthorized {detail: "Token expired"}
    end
```

**Возможные ошибки:**
- `401 Unauthorized` — Токен неверный или истек
- `401 Unauthorized` — Токен отсутствует в заголовках

---

### 4. Здоровье сервера (Health Check)

**Endpoint:** `GET /health`

**Описание:** Проверка работоспособности API сервера.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

**Состояние взаимодействия:**

```mermaid
sequenceDiagram
    participant Client as Client (Browser)
    participant API as FastAPI App

    Client->>API: GET /health
    API-->>Client: 200 {status: "ok"}
```

---

### 5. Главная страница (Root)

**Endpoint:** `GET /`

**Описание:** Главная страница API, показывает приветственное сообщение.

**Headers (опционально):**
```
Authorization: Bearer <ACCESS_TOKEN>
```

**Response (200 OK) - без авторизации:**
```json
{
  "message": "Welcome to TupolevITChallenge2026 API"
}
```

**Response (200 OK) - с авторизацией:**
```json
{
  "message": "Welcome to TupolevITChallenge2026 API, john_doe"
}
```

**Состояние взаимодействия:**

```mermaid
sequenceDiagram
    participant Client as Client (Browser)
    participant API as FastAPI App
    participant Security as Security Module
    participant UserService as User Service
    participant DB as PostgreSQL

    Client->>API: GET / [Headers: Authorization: Bearer <token>?]
    alt Has Authorization Header
        API->>Security: validate JWT token
        alt Token Valid
            Security-->>API: user_id = 1
            API->>UserService: get_by_id(user_id)
            UserService->>DB: SELECT username FROM users WHERE id = ?
            DB-->>UserService: john_doe
            UserService-->>API: user
            API-->>Client: 200 {message: "Welcome... john_doe"}
        else Token Invalid
            API-->>Client: 200 {message: "Welcome..."}
        end
    else No Authorization
        API-->>Client: 200 {message: "Welcome to TupolevITChallenge2026 API"}
    end
```

---

### Архитектура системы

```mermaid
graph TB
    Client["Client<br/>(Browser/Mobile)"]
    FastAPI["FastAPI Application<br/>Port 8000"]
    Auth["Auth Endpoints<br/>/api/auth/*"]
    UserService["User Service<br/>Business Logic"]
    Security["Security Module<br/>JWT & Password"]
    Database["PostgreSQL<br/>Database"]
    Cache["JWT Validation<br/>Cache"]
    
    Client -->|HTTP Requests| FastAPI
    FastAPI --> Auth
    Auth --> Security
    Security --> Cache
    Auth --> UserService
    UserService --> Database
    
    style Client fill:#e1f5ff
    style FastAPI fill:#fff3e0
    style Auth fill:#f3e5f5
    style UserService fill:#e8f5e9
    style Database fill:#fce4ec
    style Security fill:#fff8e1
```
