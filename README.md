# Кейс от MediaWise: Поиск файлов с помощью векторной базы данных

Наш проект решает задачу, поставленную в кейсе цифрового прорыва от MediaWise по быстрому поиску релевантных источников и генерации ответа.

## Установка зависимостей
```bash
pip install -r requirements.txt
```
## Описание данных

Изначально нам были даны 70 pdf файлов с различной информацией.\
**Пример:**
```
0.pdf
1.pdf
...
69.pdf
```

# Структура проекта

- **config**  
  Директория, содержащая конфигурационные файлы проекта.

- **data_converter**  
  Модуль для конвертации папки с файлами (PDF, TXT) в формат CSV.

- **database**  
  Директория для хранения и поддержки базы данных.

- **embeddings**  
  Модуль для работы с **chroma** (векторная база данных). Используется для хранения и быстрого доступа к векторным представлениям данных.

- **llm**  
  Директория с настройкой инференса модели.

- **utils**  
  Вспомогательные функции для поддержки основного кода.

- **Bot.py**  
  Скрипт для запуска телеграм-бота.

- **requirements.txt**  
  Файл со списком зависимостей для установки проекта.



 **GUIDE** - субдиректория для быстрого старта решения
 ```bash
 https://drive.google.com/drive/folders/1qETmaGTL9MIYJGq2BFO_tMjENgYwANz5?usp=sharing
 ```
## Структура субдиректории GUIDE

- **retriver**  
  Модуль для поиска по векторной базе данных.

- **inference**  
  Модуль для вывода ответа клиенту. Содержит логику генерации или форматирования ответа на основе данных из базы.

- **function_helpers**  
  Вспомогательные функции, поддерживающие основной код.
- **embeddings**  
  Модуль для работы с **chroma** (векторная база данных). Используется для хранения и быстрого доступа к векторным представлениям данных.

- **Data**  
  Папка для хранения данных, включая исходные. подходит для любых данных, используемых в процессе работы.

- **guide.ipynb**  
  Jupyter Notebook с подробным руководством по запуску решения. Этот ноутбук можно использовать при развёртывании и настройке проекта.

## Быстрый старт
1. **Запуск guide.ipynb**:
    Откройте `guide.ipynb` для ознакомления с инструкциями по использованию и развёртыванию системы.
2. **Запуск бота**
    Установите зависимости **requirements.py**.
    Запустите с помощью команды:
    ```
    python Bot.py
    ```

## Примечания
- Убедитесь в ваших API ключах перед запуском
