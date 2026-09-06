
# Проект: утилиты для банковских операций

Набор функций для обработки данных банковских операций: фильтрация и сортировка, маскирование номеров карт и счетов, форматирование дат, генерация человекочитаемого описания операции.

## Структура проекта

project/
├── src/
│ ├── masks.py # маскирование карт и счетов
│ ├── processing.py # filter_by_state, sort_by_date
│ └── widget.py # публичные функции: mask_*, get_date, process_data
├── tests/
│ ├── conftest.py # фикстуры
│ ├── test_masks.py
│ ├── test_processing.py
│ └── test_widget.py
├── pytest.ini # настройки тестов и покрытия
└── requirements.txt # зависимости

text

## Требования

- Python 3.9+
- Poetry (или venv)
- pytest, pytest-cov

## Установка

### Вариант с Poetry (рекомендуется)

```bash
poetry install
Poetry создаст виртуальное окружение и установит зависимости из pyproject.toml.

Вариант с venv
bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
Быстрый старт: примеры использования
Маскирование номеров
python
from src.widget import mask_account_card

print(mask_account_card("Visa 7000123456789012"))
# Visa 7000 12** **** 9012

print(mask_account_card("Счёт 40817810000012345678"))
# Счёт **5678
Фильтрация и сортировка операций
python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
    {"id": 2, "state": "PENDING",  "date": "2024-03-10"},
    {"id": 3, "state": "EXECUTED", "date": "2023-12-01"},
]

executed = filter_by_state(operations, "EXECUTED")
sorted_ops = sort_by_date(executed, reverse=True)
Человекочитаемое описание операции
python
from src.widget import process_data

operation = {
    "date": "2024-09-10T12:34:56.123456",
    "description": "Перевод между счетами",
    "from": "Card 7000123456789012",
    "to": "Account 40817810000012345678",
    "operationAmount": {"amount": 5000, "currency": {"name": "RUB"}},
}

print(process_data(operation))
# 10.09.2024 Перевод между счетами
# Card 7000 12** **** 9012 -> Account **5678
# 5000 RUB
Тестирование
Запуск всех тестов:

bash
pytest
Запуск с проверкой покрытия (минимум 80%):

bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
HTML-отчёт о покрытии:

bash
pytest --cov=src --cov-report=html
# затем открыть htmlcov/index.html в браузере
Тесты используют параметризацию и фикстуры из tests/conftest.py и покрывают:

маскирование карт (разные длины, граничные случаи)
маскирование счетов (ровно 20 цифр)
фильтрацию по полю state
сортировку по дате (валидные и невалидные даты)
обработку некорректных входных данных
Особенности реализации
Маскирование без регулярных выражений: логика построена на подсчёте цифр и ручной подстановке символов.
Обработка дат: поддерживается несколько форматов (ISO, YYYY-MM-DD, YYYY/MM/DD, DD.MM.YYYY) с автоматическим поиском даты в строке и конвертацией в ДД.ММ.ГГГГ.
Безопасность: функции не падают на некорректных типах входных данных, а возвращают исходные значения или пустые результаты.
Стабильная сортировка: при одинаковых датах порядок элементов сохраняется.
Рекомендации по развитию
Добавить интеграционные тесты на полный пайплайн: получение списка → фильтрация → сортировка → форматирование → вывод.
Расширить поддержку валют и форматов сумм.
Вынести конфигурацию (например, правила маскирования) в отдельный модуль или конфиг-файл.
Лицензия
MIT (или укажите свою)