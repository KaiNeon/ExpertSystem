import time
import logging
from kb_module import KnowledgeBase


class Task:
    def __init__(self, knowledge_base: KnowledgeBase):
        """Инициализация текущей задачи"""
        self.kb = knowledge_base
        self.accepted_facts = []
        self.rejected_facts = []

    def question(self, fact_id):
        """Задать вопрос пользователю в терминале"""
        time.sleep(0.1)
        fact_info = self.kb.get_verbal('facts', [fact_id])[0]

        print(f"\nСуществует утверждение:")
        print(f"\tНомер в базе:\t{fact_info[0]}")
        print(f"\tНаименование:\t{fact_info[1]}")
        print(f"\tИнформация:  \t{fact_info[2]}")
        answer = input(f"Это утверждение относится к вашей проблеме?\nВвод: ")

        if answer.lower() in "yesofcoursetrueдаправда":
            self.accepted_facts.append(fact_id)
            logging.info(f"fact [{fact_id}] accepted")
        else:
            self.rejected_facts.append(fact_id)
            logging.info(f"fact [{fact_id}] rejected")

    def _available_solutions(self):
        # Отсеивание решений, включающих отрицаемые факты
        solutions = self.kb.list_difference(
            self.kb.select_solutions(self.accepted_facts),
            self.kb.select_rej_solutions(self.rejected_facts)
        )
        # При отсутствии доступных решений повторная выборка от обратного
        if not solutions:
            logging.info(f"[task]\tsolution select from opposite")
            solutions = self.kb.list_difference(
                self.kb.all_solutions(), self.kb.select_rej_solutions(self.rejected_facts)
            )
        return solutions

    def _most_popular_solution(self, available_solutions):
        """Выбор наиболее популярного решения из списка"""
        return self.kb.max_vote_up(available_solutions)[0]

    def _possible_facts(self, solution_id):
        """Получение списка id доступных фактов"""
        facts_union = KnowledgeBase.list_union(self.accepted_facts, self.rejected_facts)
        return list(
            KnowledgeBase.list_difference(
                self.kb.select_facts(solution_id), facts_union
            )
        )

    def get_answer(self):
        """Получение списка возможных решений (при окончании поиска)"""
        logging.info(f"accepted facts: {self.accepted_facts}")
        logging.info(f"rejected facts: {self.rejected_facts}")
        result = self._available_solutions()
        logging.info(f"final answer:\t{result}")
        time.sleep(0.1)
        return result

    def find_solution_step(self):
        """Шаг поиска решения задачи"""
        logging.info(f"available solutions:\t{self._available_solutions()}")

        # осталось одно доступное решение = решение является ответом
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
