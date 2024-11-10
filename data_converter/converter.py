import os
import io
import fitz
import pandas as pd
import shutil
from typing import Optional


def create_text_dataset(folder_path: str = f"{os.getcwd()}/files/temp") -> Optional[pd.DataFrame]:
    """Функция для создания датасета из PDF и TXT файлов.

    Args:
        folder_path (str): Путь к папке с PDF и TXT файлами

    Returns:
        pd.DataFrame: Датасет с колонками ['file_name', 'page_number', 'text']
    """

    # Список для данных
    data = []

    # Получаем список всех PDF и TXT файлов в папке
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.pdf', '.txt'))]

    # Обрабатываем каждый файл
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            if file.lower().endswith('.pdf'):
                # Обработка PDF файлов
                with fitz.open(file_path) as pdf:
                    for page_num in range(len(pdf)):
                        page = pdf[page_num]
                        text = page.get_text()
                        if text.strip():  # Проверяем, что текст не пустой
                            data.append({
                                'file_name': file,
                                'page_number': page_num + 1,
                                'text': text
                            })
                print(f"Успешно обработан PDF файл: {file}")
            elif file.lower().endswith('.txt'):
                # Обработка TXT файлов
                with open(file_path, 'r', encoding='utf-8') as txt_file:
                    text = txt_file.read()
                    if text.strip():  # Проверяем, что текст не пустой
                        # В текстовом файле нет страниц, поэтому используем номер 1 для всех строк
                        data.append({
                            'file_name': file,
                            'page_number': 1,
                            'text': text
                        })
                print(f"Успешно обработан TXT файл: {file}")
                shutil.move(file_path, f"{os.getcwd()}/files/knowledge")
        except Exception as e:
            print(f"Ошибка при обработке файла {file}: {str(e)}")
            return None

    # Создаем DataFrame с данными
    df = pd.DataFrame(data, columns=['file_name', 'page_number', 'text'])

    print(f"Создан датасет с {len(df)} строками")

    return df


def pdf_page_to_image(pdf_name: str, page_number: int, pdf_dir: str = f"{os.getcwd()}/files/knowledge") -> Optional[io.BytesIO]:
    """Функция для получения страницы пдф

    Args:
        pdf_dir (str): Директория с пдф
        pdf_name (str): Имя файла
        page_number (int): Номер страницы в файл

    Returns:
        Optional[io.BytesIO]: Изображение как байты
    """
    pdf_path = os.path.join(pdf_dir, pdf_name)

    # Проверка, что файл существует
    if not os.path.exists(pdf_path):
        print(f"Файл '{pdf_path}' не найден.")
        return None

    # Проверяем, что номер страницы корректен
    doc = fitz.open(pdf_path)
    if page_number < 0 or page_number >= doc.page_count:
        print(f"Некорректный номер страницы. Допустимый диапазон: 0 - {doc.page_count - 1}")
        doc.close()
        return None
    
    page = doc.load_page(page_number)    
    pix = page.get_pixmap()
    doc.close()


    image_bytes = io.BytesIO()
    img = io.BytesIO(pix.tobytes("png"))
    return img