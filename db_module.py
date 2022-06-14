import logging
import sqlite3


# Класс для работы с базой данных
class DataBase:
    def __init__(self, path='KnowledgeBase.db'):
        self.path = path

    @staticmethod
    def open_tuple(data: list):
        return [elem for elem in data]

    @staticmethod
    def open_tuple_list(data: list):
        return [DataBase.open_tuple(elem) for elem in data]

    def _connect(self):
        return sqlite3.connect(self.path)

    def modify_request(self, query: str):
        """Обновление информации в базе по запросу"""
        db = self._connect()
        cursor = db.cursor()
        query = query
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()

    def broad_select_request(self, query: str):
        """Выборка списка по запросу"""
        db = self._connect()
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return records

    def single_select_request(self, query: str):
        """Выборка единичной строки по запросу"""
        db = self._connect()
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchone()
        cursor.close()
        db.close()
        return self.open_tuple(records)

    def selection_by_column_in_values(self, selection: list, table: str, column: str, values: list):
        """Генерация запроса выборки"""
        if selection:
            selection = ", ".join(selection)
        else:
            selection = "*"
        values = ", ".join([str(value) for value in values])
        condition = f"WHERE {column} IN ({values})"
        result = self.broad_select_request(f"""
            SELECT {selection} FROM {table} {condition}
        """)
        logging.debug(f"[db][SELECT]\t{result}")
        return result
