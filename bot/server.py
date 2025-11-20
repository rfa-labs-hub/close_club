from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.getenv('BOT_TOKEN', '8528257183:AAGj_C6DrpFIFt6hYOTCgKBOL4vOmCpLIl0')
GROUP_ID = os.getenv('GROUP_ID', '-1003464615752')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def escape_html(value: str) -> str:
    if not value:
        return ''
    return (value.replace('&', '&amp;')
                 .replace('<', '&lt;')
                 .replace('>', '&gt;')
                 .replace('"', '&quot;')
                 .replace("'", '&#039;'))


def send_message(message: str):
    try:
        response = requests.post(
            f'{TELEGRAM_API_URL}/sendMessage',
            json={
                'chat_id': GROUP_ID,
                'text': message,
                'parse_mode': 'HTML'
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if not data.get('ok', False):
            return False, data
        return True, data
    except requests.RequestException as exc:
        error_payload = exc.response.json() if getattr(exc, 'response', None) else {'description': str(exc)}
        print('Ошибка отправки в Telegram:', error_payload)
        return False, error_payload


@app.post('/api/submit-application')
def submit_application():
    data = request.get_json() or {}

    name = data.get('name', '').strip()
    telegram = data.get('telegram', '').strip()
    message_text = data.get('message', '').strip()

    if not all([name, telegram, message_text]):
        return jsonify({'success': False, 'error': 'Все поля обязательны'}), 400

    formatted_message = f"""
<b>📋 Новая заявка</b>

<b>Имя:</b> {escape_html(name)}
<b>Telegram:</b> {escape_html(telegram)}
<b>Сообщение:</b>
{escape_html(message_text)}

<i>Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
""".strip()

    success, result = send_message(formatted_message)

    if success:
        return jsonify({'success': True, 'message': 'Заявка отправлена'}), 200

    return jsonify({'success': False, 'error': result.get('description', 'Не удалось отправить в Telegram')}), 500


@app.get('/api/ping')
def ping():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(f'Сервер запущен: http://localhost:{port}')
    print(f'Bot token: {BOT_TOKEN[:10]}...  Group ID: {GROUP_ID}')
    app.run(host='0.0.0.0', port=port)

