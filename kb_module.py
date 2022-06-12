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

    def select_facts(self, solution_id):
        return self.open_single_tuples(
            self.db.selection_by_column_in_values(['fact_id'], 'pairs', 'solution_id', [solution_id])
        )

    def select_solutions(self, facts):
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
        return self.open_single_tuples(
            self.db.selection_by_column_in_values(['solution_id'], 'pairs', 'fact_id', facts)
        )

    def get_verbal(self, table, id_list):
        return self.db.open_tuple_list(
            self.db.selection_by_column_in_values(['id', 'name', 'info'], table, 'id', id_list)
        )

    def get_all_pairs_verbal(self):
        return self.db.broad_select_request(f"""
            SELECT pairs.id as pair_id, facts.name as fact_name, solutions.name as solution_name
            FROM pairs
            JOIN facts ON pairs.fact_id=facts.id
            JOIN solutions ON pairs.solution_id=solutions.id
        """)
