import categories
import db

from exceptions import NotCorrectMessage
from typing import NamedTuple
from datetime import datetime


class Task(NamedTuple):
    """Структура задания"""
    date: str
    category_codename: str
    text: str


def get_tasks_by_date(date: str) -> list[Task]:
    _parse_date(date)
    result = db.fetchall('tasks', ['category', 'text'], f'date = "{date.replace(".", "-")}"')
    tasks = []
    for rs in result:
        tasks.append(Task(
            date=date,
            category_codename=rs["category"],
            text=rs["text"]
        ))

    return tasks


def add_todo(message: str, user_id: str) -> Task:
    """Добавить задание в базу данных"""
    task = _parse_message(message)
    db.insert('tasks', {
        'user_id': user_id,
        'category': task.category_codename,
        'date': task.date.replace(".", "-"),
        'text': task.text
    })
    return task


def _parse_message(message: str) -> Task:
    _split_message = message.split()
    if len(_split_message) < 3:
        raise NotCorrectMessage("Сообщение должно содержать дату, категорию и текст.")

    if len(' '.join(_split_message[2:])) < 3:
        raise NotCorrectMessage("Текст задания должен содержать больше трех символов")

    task = Task(
        date=_parse_date(_split_message[0]),
        category_codename=_parse_category(_split_message[1]).codename,
        text=' '.join(_split_message[2:])
    )

    return task


def _parse_category(alias: str) -> categories.Category:
    return categories.Categories().get_category(alias)


def _parse_date(data: str) -> str:
    try:
        datetime.strptime(data, '%d.%m.%Y')
        return data
    except ValueError:
        raise NotCorrectMessage("Введите дату в формате ДД.ММ.ГГГГ")
