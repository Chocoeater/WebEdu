# 🎓 WebEdu - backend образовательной платформы

 Backend на Django + DRF для онлайн-обучения: курсы, уроки, подписки на обновления, покупки уроков/курсов через Stripe, уведомления по почте и работа фоновых задач через Celery.
 
---

## Основной функционал

### Пользователи (`users`)

Кастомная модель `User` на основе `AbstractUser`:

- логин по **email** (поле `username` отключено);
- `avatar` аватар пользователя (ImageField, папка `users/avatars`);
- `phone` номер телефона (`PhoneNumberField`);
- `country` страна пользователя;
- `last_login` обновляется автоматически при логине (используется для деактивации через Celery).

Основные возможности:

- регистрация нового пользователя;
- авторизация по JWT (SimpleJWT);
- просмотр и обновление профиля;
- список пользователей (с фильтрацией правами);
- частичное и полное удаление (для админов).

JWT-получение токенов:

```http
POST /users/token/
{
  "email": "user@example.com",
  "password": "qwerty123"
}
```
В ответ приходит пара токенов (access / refresh), которые используются в заголовке:
Authorization: Bearer <access_token>.

### Курсы и уроки (materials)
Приложение materials отвечает за учебные материалы.

- Модель `Course`
  - `name` название курса;
  
  - `preview` картинка-превью (необязательно);
  
  - `description` описание курса.

- Модель `Lesson`
  - `name` название урока;
  
  - `preview` превью (необязательно);
  
  - `description` описание;

  - `link` ссылка на видео только YouTube (проходит валидацию через LinkValidator);
  
  - `course` курс, к которому относится урок;
  
  - `owner` владелец (пользователь).

- Модель `Subscription`
  - `user` пользователь;
  
  - `course` курс, на который он подписан.

### Подписки и уведомления
Подписки реализованы через Subscription и эндпоинт:

```http
POST /subscriptions/
{
  "id": 1    // ID курса
}
```
Поведение:

- если пользователь не подписан - создаётся подписка, отправляется письмо «Подписка добавлена»;

- если подписан - подписка удаляется, отправляется письмо «Подписка удалена».

- Письма отправляются через Celery-таску send_about_sub.

При обновлении курса (PUT/PATCH по /courses/{id}/) всем подписчикам курса уходит письмо через таску send_update_sub.

### Платежи и Stripe
Модель `Payment`:

  - `user` кто оплатил;
  
  - `date_of_pay` дата платежа (авто);
  
  - `paid_course` оплаченный курс (опционально);
  
  - `paid_lesson` оплаченный урок (опционально);
  
  - `payment_amount` сумма в рублях;
  
  - `payment_method` "cash" или "transfer";
  
  - `link_for_pay` ссылка на оплату (Stripe Checkout);
  
  - `session_id` ID сессии Stripe.

### Создание платежа:

```http
POST /users/payments/create/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "paid_course": 1,
  "payment_amount": 5000,
  "payment_method": "transfer"
}
```
Во время `perform_create`:

- сумма в рублях конвертируется в доллары (заглушка курса в convert_rub_to_usd);

- создаётся Product и Price в Stripe;

- создаётся сессия Stripe Checkout;

- в `payment.link_for_pay` сохраняется URL оплаты, а в `session_id` ID сессии.

Клиенту остаётся перейти по `link_for_pay` и завершить оплату.

### Фоновые задачи (Celery)
Есть отдельный модуль задач:

- `users.tasks.deactivate_inactive_users` раз в 30 дней (в проекте стоит каждые 30 секунд для теста) деактивирует пользователей, которые не логинились больше месяца;

- `materials.tasks.send_about_sub` уведомление о подписке/отписке;

- `materials.tasks.send_update_sub` уведомление об обновлении курса.

Celery настраивается через config/celery.py, используется django-celery-beat.

## Структура проекта
```text
WebEdu/
├── config/               # Настройки Django, Celery, URLs, Swagger
├── materials/            # Курсы, уроки, подписки
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── validators.py
│   └── urls.py
├── users/                # Пользователи и платежи
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── services.py       # Логика Stripe
│   ├── management/
│   │   └── commands/
│   │       └── add_admin.py
│   └── urls.py
├── templates/            # HTML-шаблоны (если используются)
├── static/               # Статика
├── media/                # Загружаемые файлы (аватары, превью)
├── users_fixture.json    # Фикстура пользователей
├── pyproject.toml        # Конфигурация Poetry
└── manage.py
```
---

## Документация API
В проекте подключён Swagger/Redoc (drf-yasg):

- Swagger UI: http://127.0.0.1:8000/swagger/

- Redoc: http://127.0.0.1:8000/redoc/

---

## Запуск проекта
1. Предварительные требования
- Python 3.13+ (или 3.11+, если собирать руками);

- PostgreSQL (для базы данных);

- Redis (как брокер для Celery, рекомендовано);

- Аккаунт в Stripe + API-ключ;

- SMTP-почта (например, Gmail/Yandex/другой провайдер).

2. Клонирование репозитория
```bash
git clone <url-репозитория>
cd WebEdu
```
3. Установка зависимостей (Poetry)
```bash
poetry install
```
Активируем окружение (если нужно):

```bash
poetry shell
```
4. Настройка переменных окружения
Скопируйте пример файла окружения:

```bash
cp .env.exemple .env
```
Заполните .env:

```env
# PostgreSQL
NAME_BD=webedu
HOST_BD=localhost
USER_BD=postgres
PASSWORD_BD=postgres
PORT_BD=5432

# Stripe
STRIPE_API_KEY=<твой_секретный_stripe_key>

# SMTP
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=webedu@example.com
EMAIL_HOST_PASSWORD=super_secret_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```
Также для Celery удобно выставить брокер через переменную окружения (например, Redis):

```env
CELERY_BROKER_URL=redis://localhost:6379/0
```
!!! **Переменная CELERY_BROKER_URL читается самим Celery из окружения, в settings.py она не прописана - достаточно задать её в .env или окружении вашей ОС.**

5. Настройка базы данных
Создайте БД в PostgreSQL (пример):

```bash
psql -U postgres -c "CREATE DATABASE webedu;"
```
Примените миграции:

```bash
poetry run python manage.py migrate
```
При необходимости загрузите тестовых пользователей:

```bash
poetry run python manage.py loaddata users_fixture.json
```
Создайте администратора (через команду/стандартно):

```bash
poetry run python manage.py add_admin
# или
poetry run python manage.py createsuperuser
```
6. Запуск Django-сервера
```bash
poetry run python manage.py runserver
```
По умолчанию сервер будет доступен по адресу:
http://127.0.0.1:8000/

7. Запуск Celery
7.1. Запуск Redis (пример через Docker)
```bash
docker run -d -p 6379:6379 --name redis redis:7
```
7.2. Запуск Celery worker
```bash
poetry run celery -A config worker -l INFO
```
7.3. Запуск Celery beat (планировщик)
```bash
poetry run celery -A config beat -l INFO
```
После этого:

будет раз в 30 секунд (в тестовом режиме) выполняться таска деактивации неактивных пользователей;

будут отрабатываться таски отправки email при подписке/обновлении курса.

---

## Тесты
Для запуска тестов:

```bash
poetry run pytest
```

---

## Используемый стек
- Python 3.13+

- Django 5.x

- Django REST Framework

- PostgreSQL

- Celery + django-celery-beat

- Redis (как брокер задач)

- Stripe (платежи)

- drf-yasg (Swagger / Redoc)

- django-phonenumber-field

- Pillow

- pytest
