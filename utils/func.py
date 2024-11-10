import asyncio
from pandas import DataFrame

from database.handlers import add_user, get_user, log_message
from embeddings.retriver import search, add_to_chroma
from data_converter.converter import create_text_dataset, pdf_page_to_image
from llm.chat_gpt import get_response
#from llm.gchat import get_response

async def preprocess_message(user_id: int, username: str, text: str) -> None:
    """Функция для обработки сообщения пользователя

    Args:
        user_id (int): id пользоваателя в телеграмме
        username (str): Тег пользователя
        text (str): Текст сообщения
    """
    user = await get_user(user_id)

    if user == None:
        await add_user(user_id, username)

    if len(text) > 0:
        asyncio.create_task(log_message(sender_id=user_id, text=text))


async def process_files() -> None:
    """
    Функция для обработки файлов от пользователей
    """

    df = await asyncio.to_thread(create_text_dataset)

    if type(df) == DataFrame:
        asyncio.create_task(asyncio.to_thread(add_to_chroma, df))
        return "Файлы успешно приняты на обработку"
    else:
        return "Не удалось обработать полученные файлы"


async def get_answer(query: str) -> dict:
    """Обёрточная функция для получения ответа на вопрос и поиска документов

    Args:
        query (str): Ввод пользователя

    Returns:
        dict: Ответ системы
    """

    entry_template = (
        "Название документа: {file_name}\n"
        "Страница в документе: {page_number}\n"
        "Уровень совпадения: {similarity_score}\n"
        "Текст:\n{text}\n"
    )

    answer_dict = await asyncio.to_thread(search, query)
    llm_query = ""

    llm_query = "\n".join(
        [
            entry_template.format(
                file_name=answer["file_name"],
                page_number=answer["page_number"],
                similarity_score=answer["similarity_score"],
                text=answer["text"],
            )
            for answer in answer_dict
        ]
    )
    llm_answer = await asyncio.create_task(get_response(query=query, context=llm_query))
    image = await asyncio.to_thread(pdf_page_to_image, answer_dict[0]["file_name"], answer_dict[0]["page_number"])

    return {
        "llm_answer": llm_answer,
        "llm_query": llm_query,
        "image": image
    }