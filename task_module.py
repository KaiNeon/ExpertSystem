import time
import logging
from kb_module import KnowledgeBase


class Task:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.accepted_facts = []
        self.rejected_facts = []
        # Не стоит проверять факт повторно, если пользователь не знает ответа
        self.last_fact = []

    def question(self, fact_id):
        # Тестовое, без интерфейса
        fact_info = self.kb.get_verbal('facts', [fact_id])[0]
        print(f"Существует утверждение:")
        print(f"\tНомер в базе:\t{fact_info[0]}")
        print(f"\tНаименование:\t{fact_info[1]}")
        print(f"\tИнформация:  \t{fact_info[2]}")
        answer = input(f"Это утверждение относится к вашей проблеме?\nВвод: ")
        if answer.lower() in "yesofcoursetrueдаправда":
            self.accepted_facts.append(fact_id)
            logging.info(f"fact [{fact_id}] rejected")
        else:
            self.rejected_facts.append(fact_id)
            logging.info(f"fact [{fact_id}] accepted")

    def _available_solutions(self):
        solutions = self.kb.list_difference(
            self.kb.possible_solutions(self.accepted_facts),
            self.kb.possible_solutions(self.rejected_facts)
        )
        if not solutions:
            solutions = self.kb.list_difference(
                self.kb.all_solutions(), self.kb.possible_solutions(self.rejected_facts)
            )
        return solutions

    def _most_popular_solution(self, available_solutions):
        return self.kb.max_vote_up(available_solutions)[0]

    def _possible_facts(self, solution_id):
        facts_union = KnowledgeBase.list_union(self.accepted_facts, self.rejected_facts)
        return list(
            KnowledgeBase.list_difference(
                self.kb.possible_facts(solution_id), facts_union
            )
        )

    def get_answer(self):
        result = self._available_solutions()
        logging.info(f"final answer:\t{result}")
        time.sleep(0.1)
        return result

    def find_solution_step(self):
        logging.info(f"available solutions:\t{self._available_solutions()}")
        # Целевое решение не меняется, починить

        available_solutions = self._available_solutions()
        if len(available_solutions) == 1:
            logging.info(f"last available solution")
            return True

        target_solution_id = self._most_popular_solution(available_solutions)
        logging.info(f"target solution:\t{[target_solution_id]}")

        target_fact_range = self._possible_facts(target_solution_id)
        logging.info(f"possible facts:\t{target_fact_range}")

        # закончились доступные факты = последняя цель является ответом
        if not target_fact_range:
            logging.info(f"run out of available facts")
            return True

        target_fact_id = self.kb.random_element(target_fact_range)

        time.sleep(0.1)
        self.question(target_fact_id)

        # закончились доступные решения = прекратить поиск
        if not self._available_solutions():
            logging.info(f"run out of available solutions")
            return True

        return False
