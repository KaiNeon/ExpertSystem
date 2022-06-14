# Импорт необходимых библиотек и модулей
import logging
import random
from db_module import DataBase


# Класс для ...
class KnowledgeBase:
    def __init__(self, db: DataBase):
        self.db = db

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

    def increment_solution_vote_up(self, solution_id):
        old_values = self.db.open_tuple_list(
            self.db.selection_by_column_in_values(['vote_up', 'vote_count'], 'solutions', 'id', [solution_id])
        )[0]
        self.db.modify_request(f"""
            UPDATE solutions SET vote_up={old_values[0] + 1}, vote_count={old_values[1] + 1} WHERE id={solution_id}
        """)

    def all_solutions(self):
        """Получение id всех решений в базе"""
        return self.open_single_tuples(
            self.db.broad_select_request(f"""
                SELECT id FROM solutions
            """)
        )

    def max_vote_up(self, solutions_range):
        """Получение решения с максимальной оценкой"""
        values = ", ".join([str(value) for value in solutions_range])
        return self.db.single_select_request(f"""
            SELECT id FROM solutions WHERE id IN ({values}) ORDER BY vote_up DESC
        """)

    def select_facts(self, solution_id):
        """Выборка фактов на основании решений"""
        return self.open_single_tuples(
            self.db.selection_by_column_in_values(['fact_id'], 'pairs', 'solution_id', [solution_id])
        )

    def select_solutions(self, facts):
        """Выборка решений на основании фактов"""
        solutions = self.open_single_tuples(
            self.db.selection_by_column_in_values(['solution_id'], 'pairs', 'fact_id', facts)
        )
        # Отсеивание неполных совпадений
        result = []
        for solution in solutions:
            if solution not in result:
                if solutions.count(solution) == len(facts):
                    result.append(solution)
        logging.debug(f"[kb][POSSIBLE_SOL]\t{result}")
        return result

    def select_rej_solutions(self, facts):
        """Выборка решений на основании фактов (отвергнутые)"""
        return self.open_single_tuples(
            self.db.selection_by_column_in_values(['solution_id'], 'pairs', 'fact_id', facts)
        )

    def get_verbal(self, table, id_list):
        """Получение дополнительной (читаемой) информации по факту или решению"""
        return self.db.open_tuple_list(
            self.db.selection_by_column_in_values(['id', 'name', 'info'], table, 'id', id_list)
        )

    def get_all_pairs_verbal(self):
        """Получение читаемой информации по всем парам (факт/решение)"""
        return self.db.broad_select_request(f"""
            SELECT pairs.id as pair_id, facts.name as fact_name, solutions.name as solution_name
            FROM pairs
            JOIN facts ON pairs.fact_id=facts.id
            JOIN solutions ON pairs.solution_id=solutions.id
        """)
