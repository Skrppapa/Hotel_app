# API для бронирования отелей (Hotel Booking API)

REST API сервис для поиска и бронирования номеров в отелях. Проект разрабатывается в рамках курса «Backend разработка на Python» (PyTex) с упором на чистую архитектуру и современные стандарты веб-разработки.

## 🛠 Технологии и стек

**Язык и фреймворки:**
* Python 3.10+
* FastAPI
* Pydantic (валидация данных)

**Базы данных и ORM:**
* PostgreSQL (основная реляционная БД)
* SQLAlchemy (взаимодействие с БД)
* Alembic (управление миграциями)
* Redis (кэширование данных и брокер для Celery)

**Инфраструктура и фоновые задачи:**
* Docker & Docker Compose (контейнеризация)
* Celery (асинхронные задачи: обработка изображений отелей)
* JWT (аутентификация и авторизация)

**Тестирование:**
* Pytest (юнит- и интеграционные тесты)

## ⚙️ Реализованный функционал
* **Пользователи:** Регистрация, аутентификация по JWT-токену, управление профилем.
* **Отели и номера:** Получение списка доступных отелей, фильтрация и просмотр свободных номеров на выбранные даты.
* **Бронирование:** Создание бронирования, проверка доступности номера, защита от двойного бронирования (Race Condition).
* **Производительность:** Кэширование частых запросов с использованием Redis для ускорения времени ответа API.

## 🚀 Как запустить проект локально

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/Skrppapa/Hotel_app.git](https://github.com/Skrppapa/Hotel_app.git)
   cd Hotel_app
   ```

2. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта (пример можно посмотреть в `.env.example`) и укажите доступы к вашей БД PostgreSQL и Redis:
   ```bash
   cp .env.example .env
   ```

3. **Создайте Docker-сеть:**
   Для корректной связи контейнеров между собой необходимо создать общую сеть:
   ```bash
   docker network create myNetwork
   ```

4. **Запустите базы данных (PostgreSQL и Redis):**
   ```bash
   docker run --name booking_db \
       -p 6432:5432 \
       -e POSTGRES_USER=abcde \
       -e POSTGRES_PASSWORD=abcde \
       -e POSTGRES_DB=booking \
       --network=myNetwork \
       --volume pg-booking-data:/var/lib/postgresql/data \
       -d postgres:16

   docker run --name booking_cache \
       -p 7379:6379 \
       --network=myNetwork \
       -d redis:7.4
   ```

5. **Запустите Nginx:**
   ```bash
    docker run --name booking_nginx \
       --volume ./nginx.conf:/etc/nginx/nginx.conf \
       --network=myNetwork \
       --rm -p 80:80 nginx
   ```
6. **Запустите бэкенд и воркеры Celery:**
   Остальные сервисы поднимаются через Docker Compose:
   ```bash
   docker compose up -d --build
   ```

7. **Примените миграции базы данных:**
   *(Если они не применяются автоматически при старте бэкенда)*
   ```bash
   docker exec -it booking_back alembic upgrade head
   ```

После запуска API будет доступно по адресу: http://localhost:7777 (или по порту, указанному в конфигурации).
Интерактивная документация (Swagger): http://localhost:7777/docs