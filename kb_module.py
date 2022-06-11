# Импорт необходимых библиотек и модулей
import logging
import sqlite3
import random


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

    # Подключение базы данных
    def _connect(self):
        return sqlite3.connect(self.path)

    # Нечеткий запрос в базу данных
    def broad_select_request(self, query: str):
        db = self._connect()
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return records

    def single_select_request(self, query: str):
        db = self._connect()
        cursor = db.cursor()
        cursor.execute(query)
        records = cursor.fetchone()
        cursor.close()
        db.close()
        return self.open_tuple(records)

    def selection_by_column_in_values(self, selection: list, table: str, column: str, values: list):
        # Не очень красиво
        if selection:
            selection = ", ".join(selection)
        else:
            selection = "*"
        values = ", ".join([str(value) for value in values])
        condition = f"WHERE {column} IN ({values})"
        result = self.broad_select_request(f"""
            SELECT {selection} FROM {table} {condition}
        """)
        return result


# Класс для ...
class KnowledgeBase:
    def __init__(self, db_path):
        self.db = DataBase(db_path)

    @staticmethod
    def list_difference(first, second):
        return list(set(first) - set(second))

    @staticmethod
    def list_union(first, second):
        return list(set(first).union(set(second)))

    @staticmethod
    def random_element(elements):
        return elements[random.randrange(len(elements))]

    @staticmethod
    def open_single_tuples(data: list):
        return [elem[0] for elem in data]

    def all_solutions(self):
        return self.open_single_tuples(
            self.db.broad_select_request(f"""
                SELECT id FROM solutions
            """)
        )

    def max_vote_up(self, solutions_range):
        values = ", ".join([str(value) for value in solutions_range])
        return self.db.single_select_request(f"""
            SELECT id FROM solutions WHERE id IN ({values}) ORDER BY vote_up DESC
        """)

    def solutions_votes(self, solutions_range):
        return self.db.selection_by_column_in_values(
            ['id', 'vote_up', 'vote_down', 'vote_count'], 'solutions', 'id', solutions_range
        )

    def possible_facts(self, solution_id):
        return self.open_single_tuples(
            self.db.selection_by_column_in_values(['fact_id'], 'pairs', 'solution_id', [solution_id])
        )

    def possible_solutions(self, facts):
        return self.open_single_tuples(
            self.db.selection_by_column_in_values(['solution_id'], 'pairs', 'fact_id', facts)
        )

    def get_solution_verbal(self, solution_id):
        return self.db.open_tuple_list(
            self.db.broad_select_request(f"""SELECT * FROM solutions WHERE id={solution_id}"""))[0]

    def get_all_pairs_verbal(self):
        return self.db.broad_select_request(f"""
            SELECT pairs.id as pair_id, facts.name as fact_name, solutions.name as solution_name
            FROM pairs
            JOIN facts ON pairs.fact_id=facts.id
            JOIN solutions ON pairs.solution_id=solutions.id
        """)
