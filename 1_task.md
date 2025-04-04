# 📝 Архитектура сервиса кастомных уведомлений через Telegram

## Общее
Сервис предназначен для отправки кастомных уведомлений в Telegram с гарантией доставки **exactly-once**.

## Компоненты системы

### 1. **FastAPI**
- Принимает запросы на отправку уведомлений.
- Валидирует данные и отправляет их в очередь RabbitMQ.
- Работает асинхронно для высокой производительности.

### 2. **Очередь сообщений (RabbitMQ + Celery)**
- Гарантирует надежную доставку сообщений.
- Позволяет балансировать нагрузку между обработчиками.

### 3. **Сервис уведомлений (Notification Worker)**
- Получает сообщения из RabbitMQ.
- Отправляет их через **Telegram Bot API**.
- Записывает статус отправки в **PostgreSQL**.

### 4. **База данных (PostgreSQL)**
- Хранит статусы сообщений ("в очереди", "отправлено", "ошибка").
- Хранит уникальные индексы для предотвращения дубликатов.

### 5. **Телеграм-бот (Telegram Bot API)**
- Принимает сообщения от сервиса.
- Может отправлять обратные webhooks о статусе доставки.

### 6. **Система мониторинга (Prometheus + Grafana)**
- Логирует успешные и неуспешные сообщения.
- Позволяет отслеживать сбои и аномалии в отправке.

---
## Механизм работы

### 1. **Получение запроса**
- Клиент делает **POST**-запрос на `/send_message/` в **FastAPI**.
- API проверяет входные данные и создает запись в **PostgreSQL** со статусом `"в очереди"`.
- Сообщение ставится в очередь **RabbitMQ**.

### 2. **Обработка сообщения в Celery**
- Воркер **Celery** забирает сообщение из RabbitMQ.
- Проверяет, не было ли оно уже отправлено (гарантия exactly-once).
- Отправляет сообщение через **Telegram Bot API**.
- Если успешно, обновляет статус в БД на `"отправлено"`.

### 3. **Гарантированная доставка**
- Если обработчик упал до завершения обработки, RabbitMQ повторно отправит задачу.
- Если Telegram API не отвечает, Celery делает повторную попытку с увеличенной задержкой.
- Если пользователь заблокировал бота, фиксируем ошибку.

### 4. **Webhook от Telegram**
- Telegram может отправлять webhook с подтверждением доставки.
- Webhook обновляет статус сообщения в БД.

---
## Выбор технологий

| Компонент  | Технология       | Обоснование                                                              |
|------------|-----------------|--------------------------------------------------------------------------|
| **API**    | FastAPI          | Высокая производительность, асинхронность                                |
| **Очередь**| RabbitMQ         | Гибкость и надежность доставки                                           |
| **Воркер** | Celery           | Поддержка повторных отправок при возникновении ошибок и масштабируемость |
| **БД**     | PostgreSQL       | Поддержка транзакций и индексов                                          |
| **Мониторинг** | Prometheus + Grafana | Отслеживание метрик и ошибок                                             |

---
## Сильные и слабые стороны

### ✅ **Плюсы**
✔ Высокая производительность (асинхронность FastAPI).  
✔ **Exactly-once** доставка через транзакции PostgreSQL и Ack в RabbitMQ.  
✔ Хорошая масштабируемость за счет Celery и очередей.  
✔ Мониторинг через Prometheus + Grafana.  

### ❌ **Минусы**
⚠ RabbitMQ требует тонкой настройки Ack для исключения дубликатов.  
⚠ Telegram API имеет ограничения по частоте запросов (нужно rate-limiting).  

---

## Итог
✅ FastAPI + RabbitMQ + Celery + PostgreSQL обеспечивают гарантированную доставку уведомлений с высокой производительностью.  
✅ Можно легко масштабировать за счет увеличения воркеров.  
✅ Поддержка exactly-once за счет уникальных записей и подтверждений.  

