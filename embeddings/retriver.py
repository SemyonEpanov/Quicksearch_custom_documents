import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
import uuid
import os


client = chromadb.PersistentClient(f"{os.getcwd()}/embeddings/db")
collection = client.get_or_create_collection(name="knowledge_library")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device='cpu')
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=300, chunk_overlap=50)


def add_to_chroma(df: pd.DataFrame):
    """Функция для добавления данных в векторное хранилище

    Args:
        df (pd.DataFrame): Данныe в виде таблицы [file_name, page_number]
    """
    df = df.rename(columns={"pdf_name": "file_name"})
    for i, row in df.iterrows():
        list_of_chunks = text_splitter.split_text(row["text"])
        for chunk in list_of_chunks:
            vector = model.encode(chunk).tolist()
            collection.add(
                documents=[chunk],
                metadatas=[
                    {
                        "file_name": row["file_name"],
                        "page_number": row["page_number"],
                    }
                ],
                embeddings=[vector],
                ids=[str(uuid.uuid4())],
            )
        print(f"Обработка входных файлов в chroma завершена на {i/df.shape[0]*100}%")
    print(f"Обработка входных файлов в chroma окончена")


def search(query: str, top_k: int = 3) -> list[dict]:
    """Функция для поиска по запросы в хранилище

    Args:
        query (str): Запрос пользователя
        top_k (int, optional): Сколько лучших ответов выдать

    Returns:
        list[dict]: Ответ в формате словаря с метаданными
    """
    query_vector = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results.get("distances", [])[0]
    search_results = []

    for doc, meta, distance in zip(documents, metadatas, distances):
        search_results.append(
            {
                "text": doc,
                "file_name": meta["file_name"],
                "page_number": meta["page_number"],
                "similarity_score": (100 - distance) / 100,
            }
        )
    return search_results


def init_chroma():
    cur_path = os.getcwd()
    dataframes = []

    for file in os.listdir(f"{cur_path}/files/processed/"):
        path = f"{cur_path}/files/processed/{file}"
        try:
            df = pd.read_csv(path)
            dataframes.append(df)
            os.remove(path)
        except Exception as err:
            print(f"Файл {path} не может быть обработан.\n{err}")
    
    if len(dataframes) > 0:
        df = pd.concat(dataframes, ignore_index=True)
        add_to_chroma(df)