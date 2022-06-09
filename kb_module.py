# Импорт необходимых библиотек и модулей
import logging
import sqlite3
import random


# Класс для работы с базой данных
class DataBase:
    def __init__(self, path='KnowledgeBase.db'):
        self.path = path

    @staticmethod
    def open_tuple_list(data: list):
        result = []
        for elem in data:
            if len(elem) > 1:
                result.append(list(elem))
            else:
                result.append(elem[0])
        return result

    # Подключение базы данных
    def _connect(self):
        return sqlite3.connect(self.path)

    # Нечеткий запрос в базу данных
    def broad_request(self, query: str):
        db = self._connect()
        cursor = db.cursor()
        cursor.execute(query)
        if 'SELECT' in query:
            records = cursor.fetchall()
            cursor.close()
            db.close()
            return records
        else:
            db.commit()
            cursor.close()
            db.close()

    def selection_by_column_in_values(self, selection: list, table: str, column: str, values: list):
        # Не очень красиво
        if selection:
            selection = ", ".join(selection)
        else:
            selection = "*"
        values = ", ".join([str(fact) for fact in values])
        condition = f"WHERE {column} IN ({values})"
        result = self.broad_request(f"""
            SELECT {selection} FROM {table} {condition}
        """)
        return self.open_tuple_list(result)


# Класс для ...
class KnowledgeBase:
    def __init__(self, db_path):
        self.db = DataBase(db_path)

    def solutions_votes(self, ids):
        return self.db.selection_by_column_in_values(
            ['id', 'vote_up', 'vote_down', 'vote_count'],
            'solutions', 'id', ids
        )

    def possible_facts(self, solution_id):
        return self.db.selection_by_column_in_values(
            ['fact_id'], 'pairs', 'solution_id', [solution_id]
        )

    def possible_solutions(self, facts):
        return self.db.selection_by_column_in_values(
            ['solution_id'], 'pairs', 'fact_id', facts
        )

    @staticmethod
    def list_difference(first, second):
        return list(set(first) - set(second))

    @staticmethod
    def list_union(first, second):
        return list(set(first).union(set(second)))

    @staticmethod
    def random_element(elements):
        return elements[random.randrange(len(elements))]

    def get_solution_verbal(self, solution_id):
        return self.db.open_tuple_list(
            self.db.broad_request(f"""SELECT * FROM solutions WHERE id={solution_id}"""))[0]

    def get_all_pairs_verbal(self):
        return self.db.broad_request(f"""
            SELECT pairs.id as pair_id, facts.name as fact_name, solutions.name as solution_name
            FROM pairs
            JOIN facts ON pairs.fact_id=facts.id
            JOIN solutions ON pairs.solution_id=solutions.id
        """)
