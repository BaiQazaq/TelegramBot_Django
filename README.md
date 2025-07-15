# Telegram Django Bot

Простой Telegram-бот на Django с использованием **нативного Telegram Bot API** (`requests`, без сторонних Telegram-библиотек) и переменных окружения через `.env` (благодаря `python-decouple`).

---

## Возможности

### Команда `/start`
- Получает:
  - `chat_id`
  - `first_name`
  - `username`
- Регистрирует пользователя (`UserProfileModel`) по `telegram_chat_id`
- Обновляет имя и username
- Отвечает приветственным сообщением

### Команда `/message`
- Отправляет сообщение:
   "Это сообщение будет удалено через 5 минут для пользователя <first_name>"
- Сохраняет сообщение в базе (`MessageModel`)

### Команда `/clear`
- Ищет неудалённые сообщения младше 5 минут
- Удаляет их в Telegram (через Bot API)
- Помечает их в базе как `deleted=True`, `deleted_at=<текущее время>`

---

## Технологии

- Python 3.11.2
- Django 5.2.4
- Django REST Framework
- Telegram Bot API (`requests`)
- SQLite (по умолчанию)
- `python-decouple` — для безопасной работы с `.env`

---

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone git@github.com:BaiQazaq/TelegramBot_Django.git 
cd TelegramBot_Django
```
### 2. Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate
```
### 3. Установите зависимости
```bash
pip install -r requirements.txt
```
### 4. Настройте .env
Создайте файл .env в корне проекта:
```bash
SECRET_KEY=ваш_секретный_ключ
BOTIK_TOKEN=ваш_телеграм_бот_токен
SECRET_TOKEN=секретный_токен_для_webhook
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
Не добавляйте .env в git — он должен быть в .gitignore

### Тестирование через ngrok (локально)

1. Запустите Django-сервер
```bash
python manage.py runserver
```
2. В новом терминале — запустите ngrok:
```bash
ngrok http 8000
```
Скопируйте HTTPS-ссылку из вывода, например:
```bash
Forwarding https://9f3a-45-15-201-100.ngrok.io -> http://localhost:8000
```
В .env файл в ALLOWED_HOSTS добавить такую же часть HTTPS-ссылки - 9f3a-45-15-201-100.ngrok.io

3. Установите webhook для Telegram
Вставьте свой BOTIK_TOKEN, SECRET_TOKEN и <адрес_ngrok>:
```bash
curl -X POST "https://api.telegram.org/bot<ВАШ_БОТ_ТОКЕН>/setWebhook" \
     -d "url=https://<адрес_ngrok>/webhook/<ВАШ_SECRET_TOKEN>/"
```


## Модели

### UserProfilemodels.Model):
telegram_chat_id = models.BigIntegerField(unique=True)

first_name = models.CharField(max_length=100, blank=True, null=True)

username = models.CharField(max_length=100, blank=True, null=True)

### Message(models.Model):
user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages')

text = models.TextField()

telegram_message_id = models.BigIntegerField()

created_at = models.DateTimeField(auto_now_add=True)

deleted = models.BooleanField(default=False)

deleted_at = models.DateTimeField(blank=True, null=True)

##
Создан в рамках учебного/тестового задания.
Контакты: [Telegram - @BQazaQ]









