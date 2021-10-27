import os
import sqlite3

from typing import List, Tuple, Dict

conn = sqlite3.connect(os.path.join("db", "todo.db"), check_same_thread=False)
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str], where: str = None) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    if where is None:
        cursor.execute(f"SELECT {columns_joined} FROM {table}")
    else:
        cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {where}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def get_cursor():
    """Для написания 'сырых' запросов """
    return cursor


def _init_db():
    # TODO Костыль с try except, потом убрать
    try:
        """Инициализирует БД"""
        with open("createdb.sql", "r") as f:
            sql = f.read()
        cursor.executescript(sql)
        conn.commit()
    except:
        pass


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
