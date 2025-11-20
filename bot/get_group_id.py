import requests
import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '8528257183:AAGj_C6DrpFIFt6hYOTCgKBOL4vOmCpLIl0')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def main():
    try:
        resp = requests.get(f'{TELEGRAM_API_URL}/getUpdates', timeout=10)
        resp.raise_for_status()
        updates = resp.json().get('result', [])
        if not updates:
            print('Обновлений нет. Напишите сообщение в нужной группе и повторите.')
            return

        seen = set()
        print('Чаты, найденные в getUpdates:\n')
        for upd in updates:
            msg = upd.get('message') or upd.get('channel_post') or {}
            chat = msg.get('chat', {})
            chat_id = chat.get('id')
            if chat_id in seen or chat_id is None:
                continue
            seen.add(chat_id)
            title = chat.get('title') or chat.get('username') or chat.get('first_name') or 'без названия'
            print(f'ID: {chat_id} | тип: {chat.get("type")} | название: {title}')

    except requests.RequestException as exc:
        print('Ошибка при запросе getUpdates:', exc.response.text if getattr(exc, 'response', None) else exc)


if __name__ == '__main__':
    main()

