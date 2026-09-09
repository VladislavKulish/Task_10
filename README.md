О проекте
Проект предоставляет набор утилит для работы с банковскими операциями: фильтрация и сортировка транзакций, формирование читаемых описаний операций, генерация тестовых номеров карт. Модуль оптимизирован для использования в тестах и прототипах: все функции реализованы как генераторы для экономии памяти при работе с большими списками транзакций.

⚠️ Важно: номера карт, генерируемые card_number_generator, не являются валидными платёжными картами (отсутствует контрольная цифра по алгоритму Луна). Используйте их только для тестов и демонстраций.

Структура проекта
text
src/
  └── generators.py      # основные функции: filter_by_currency, transaction_descriptions, card_number_generator
tests/
  ├── conftest.py    # фикстуры
  └── test_generator.py # тесты функций
Установка и запуск
Требования
Python 3.9+
Poetry (рекомендуется)
Установка через Poetry
bash
poetry install
Запуск тестов с покрытием
bash
poetry run pytest --cov=src --cov-report=term-missing
Ожидаемое покрытие: не менее 80%.

Модуль src/widget.py
Модуль содержит три основные функции-генератора:

filter_by_currency(transactions, currency) — фильтрация транзакций по валюте (регистронезависимо).
transaction_descriptions(transactions) — генерация человекочитаемых описаний транзакций.
card_number_generator(start, end) — генерация номеров карт в формате XXXX XXXX XXXX XXXX.
Все функции возвращают генераторы, а не списки, что позволяет эффективно обрабатывать большие объёмы данных.

Примеры использования
Фильтрация транзакций по валюте
python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

transactions = [
    {
        "id": 1,
        "operationAmount": {"amount": 100, "currency": {"name": "USD"}}
    },
    {
        "id": 2,
        "operationAmount": {"amount": 200, "currency": {"name": "eur"}}
    },
    {
        "id": 3,
        "operationAmount": {"amount": 150, "currency": {"name": "UsD"}}
    }
]

usd_transactions = filter_by_currency(transactions, "USD")
for t in usd_transactions:
    print(t["id"])
# Вывод: 1, 3 (регистр не важен)
Особенности:

Регистронезависимое сравнение валюты.
Безопасная обработка отсутствующих ключей (не падает, просто пропускает).
Возвращает генератор.
Генерация описаний транзакций
python
from src.widget import transaction_descriptions

transactions = [
    {
        "date": "2024-05-01T12:34:56.000000",
        "description": "Перевод другу",
        "from": "Счёт 40817810000012345678",
        "to": "Карта 2200123412341234",
        "operationAmount": {"amount": 5000, "currency": {"name": "RUB"}}
    },
    {
        "date": "2024-05-02T09:15:00.000000",
        "description": "Оплата услуг",
        "to": "Счёт 40702810123456789012",
        "operationAmount": {"amount": 1200, "currency": {"name": "RUB"}}
    }
]

for desc in transaction_descriptions(transactions):
    print(desc)
Возможный вывод:

text
2024-05-01 | Перевод другу | **5678 -> **1234 | 5000 RUB
2024-05-02 | Оплата услуг | **9012 | 1200 RUB
Особенности:

Маскирует номера счетов и карт (использует внутреннюю логику маскирования).
Пропускает отсутствующие поля без ошибок.
Формат описания: [Дата] | [Описание] | [Отправитель -> Получатель] | [Сумма] [Валюта].
Возвращает генератор строк.
Генерация тестовых номеров карт
python
from src.widget import card_number_generator

gen = card_number_generator(1, 5)
for n in gen:
    print(n)
Вывод:

text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
Примеры диапазонов:

python
# Произвольный диапазон
for n in card_number_generator(1234567890123450, 1234567890123452):
    print(n)
# 1234 5678 9012 3450
# 1234 5678 9012 3451
# 1234 5678 9012 3452
Особенности:

Формат строго XXXX XXXX XXXX XXXX (16 цифр, разделённых пробелами).
Диапазон: от 1 до 9999999999999999.
Проверка на корректность диапазона (выбрасывает ValueError при недопустимых значениях).
Возвращает генератор строк.
Интеграция с другими функциями проекта
Эти функции хорошо сочетаются с ранее реализованными утилитами:

filter_by_state и sort_by_date можно применять до filter_by_currency для последовательной обработки.
Результат filter_by_currency удобно передавать в transaction_descriptions для вывода отфильтрованных операций.
card_number_generator полезен для генерации тестовых данных при написании интеграционных тестов.
Пример цепочки:

python
from src.processing import filter_by_state, sort_by_date
from src.widget import filter_by_currency, transaction_descriptions

filtered = filter_by_state(transactions, "EXECUTED")
sorted_tx = sort_by_date(filtered)
usd_tx = filter_by_currency(sorted_tx, "USD")

for desc in transaction_descriptions(usd_tx):
    print(desc)
Тестирование
Тесты написаны на pytest с использованием фикстур и параметризации. Покрытие кода — не менее 80%.

Примеры тест-кейсов:

Фильтрация по разным валютам, включая регистронезависимые варианты.
Обработка пустых списков и транзакций без валюты.
Проверка формата и последовательности номеров карт, включая граничные значения.
Валидация исключений для недопустимых диапазонов.
Запуск:

bash
poetry run pytest
Лицензия
Проект распространяется под лицензией MIT.
