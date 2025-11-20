# Telegram bot (Flask)

## Установка
```
cd bot
pip install -r requirements.txt
```

## Переменные окружения
Создайте `.env` рядом с `server.py` (опционально, значения уже подставлены по умолчанию):
```
BOT_TOKEN=8528257183:AAGj_C6DrpFIFt6hYOTCgKBOL4vOmCpLIl0
GROUP_ID=-1003464615752
PORT=3000
```

## Запуск
```
python server.py
```

Форма на сайте должна отправлять POST-запрос на `http://localhost:3000/api/submit-application`.

