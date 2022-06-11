import logging
import random
import time
from kb_module import *

logging.basicConfig(level=logging.DEBUG)


class Task:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.accepted_facts = []
        self.rejected_facts = []
        # Не стоит проверять факт повторно, если пользователь не знает ответа
        self.last_fact = []

    def question(self, fact_id):
        # Тестовое, без интерфейса
        answer = input(f"[{fact_id}] is it true?\n")
        if answer.lower() in "yesofcoursetrue":
            self.accepted_facts.append(fact_id)
            logging.info(f"new accepted fact:\t{fact_id}")
            logging.info(f"actual accepted facts:\n\t{self.accepted_facts}")
        else:
            self.rejected_facts.append(fact_id)
            logging.info(f"new rejected fact:\t{fact_id}")
            logging.info(f"actual rejected facts:\n\t{self.rejected_facts}")

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

    def _print_answer(self, solution_id):
        print(f"your solution is:\n\t{self.kb.get_solution_verbal(solution_id)[1]}"
              f"\t({self.kb.get_solution_verbal(solution_id)[2]})\n")

    def find_solution_step(self):
        logging.info(f"available solutions: {self._available_solutions()}")
        # Целевое решение не меняется, починить

        available_solutions = self._available_solutions()
        if len(available_solutions) == 1:
            logging.info(f"last available solution:\t{available_solutions[0]}")
            exit(0)

        target_solution_id = self._most_popular_solution(available_solutions)
        logging.info(f"target_solution_id:\t{target_solution_id}")

        target_fact_range = self._possible_facts(target_solution_id)
        logging.info(f"possible facts for {target_solution_id}:\n\t{target_fact_range}")

        # закончились доступные факты = последняя цель является ответом
        if not target_fact_range:
            logging.info(f"run out of available facts\nlast targeted solution:\t{target_solution_id}")
            exit(0)

        target_fact_id = self.kb.random_element(target_fact_range)

        time.sleep(0.1)
        self.question(target_fact_id)

        # закончились доступные решения = прекратить поиск
        if not self._available_solutions():
            logging.info(f"run out of available solutions")
            exit(0)

        return None


if __name__ == '__main__':
    testTask = Task(KnowledgeBase('KnowledgeBase.db'))
    while not testTask.find_solution_step():
        pass
