import asyncio.log
from telethon import TelegramClient, events
import configparser
import asyncio
import tempfile

from database.setup import init_db
from embeddings.retriver import init_chroma
from utils import func

config = configparser.ConfigParser()
config.read("config/cfg.ini", encoding="utf-8")
api_id = config["TG"].getint("api_id")
api_hash = config["TG"]["api_hash"]
bot_token = config["TG"]["bot_token"]

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage)
async def handle_new_message(event):
    # Получение данных о пользователе
    sender = await event.get_sender()
    user_id, username = sender.id, sender.username

    # Обработка сообщения
    asyncio.create_task(func.preprocess_message(user_id, username, event.raw_text))

    # Получение файлов от пользователя
    if event.message.media:
        if event.message.document.mime_type in ['application/pdf', 'text/plain']:
            await event.download_media(file="files/temp")
            result = await asyncio.create_task(func.process_files())
            await client.send_message(sender, result)
        else:
            await client.send_message(sender, "Данный формат не поддерживается.\nДопустимые форматы: **pdf, txt**")
    else:
        answer = await asyncio.create_task(func.get_answer(event.raw_text))
        await client.send_message(sender, answer["llm_answer"])
        await client.send_message(sender, answer["llm_query"])
        await client.send_file(sender, answer["image"])



if __name__=="__main__":
    # Инициаллизация бд
    asyncio.get_event_loop().run_until_complete(init_db())

    # Инициализация chroma(холодная)
    init_chroma()

    # Старт бота
    client.start()
    client.run_until_disconnected()