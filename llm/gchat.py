from gigachat import GigaChat
import configparser
import os

config = configparser.ConfigParser()
config.read(f"{os.getcwd()}/config/cfg.ini")
api_key = config["GCHAT"]["api_key"]

with open(f"{os.getcwd()}/config/compiled_prompt.txt", 'r', encoding='utf-8') as f:
    prompt = f.read()


async def get_response(query: str, context: str) -> str:
    async with GigaChat(credentials = api_key, verify_ssl_certs=False) as giga:
        response = giga.chat(f"{prompt}\n\n```{context}```\nЗапрос в систему: {query}")
        
        return response.choices[0].message.content