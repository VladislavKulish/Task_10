from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по значению ключа 'state'.

    :param operations: список словарей с данными об операциях
    :param state: значение для фильтрации (по умолчанию 'EXECUTED')
    :return: новый список словарей, где state совпадает с указанным значением
    """
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей, отсортированный по полю 'date'.

    :param operations: список словарей с данными об операциях
    :param descending: если True — сортировка по убыванию (сначала самые свежие),
                       если False — по возрастанию (сначала самые старые).
                       По умолчанию True.
    :return: отсортированный список словарей
    """
    # Даты в формате ISO ('YYYY-MM-DDTHH:MM:SS.ffffff') можно сортировать как строки — 
    # лексикографический порядок совпадает с хронологическим.
    return sorted(operations, key=lambda x: x.get('date', ''), reverse=descending)


""" Проверки функции filter_by_state
data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
]

# По умолчанию (state='EXECUTED')
result_default = filter_by_state(data)
print(result_default)
# Вывод:
# [
#   {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
# ]

# С явным указанием state='CANCELED'
result_canceled = filter_by_state(data, state='CANCELED')
print(result_canceled)
# Вывод:
# [
#   {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#   {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
# ]"""


""" Проверка функции sort_by_date
data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
]

# Сортировка по убыванию (по умолчанию)
result_desc = sort_by_date(data)
print(result_desc)
# Вывод:
# [
#   {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#   {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
#   {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
# ]

# Сортировка по возрастанию
result_asc = sort_by_date(data, descending=False)
print(result_asc)
# Вывод — в обратном порядке (от старых к новым)"""
