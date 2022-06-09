import logging
import random
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

    def _most_popular_solution(self):
        possible_solutions = self.kb.list_difference(
            self.kb.possible_solutions(self.accepted_facts),
            self.kb.possible_solutions(self.rejected_facts)
        )
        logging.info(f"possible solutions:\n\t{possible_solutions}")
        votes = self.kb.solutions_votes(possible_solutions)
        most_popular = max(votes, key=lambda solution_data: solution_data[1])[0]
        return most_popular

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
        # Целевое решение не меняется, починить

        target_solution_id = self._most_popular_solution()
        logging.info(f"target_solution_id:\t{target_solution_id}")

        target_fact_range = self._possible_facts(target_solution_id)
        logging.info(f"possible facts for {target_solution_id}:\n\t{target_fact_range}")

        if not target_fact_range:
            logging.info(f"out of possible facts")
            logging.info(f"last targeted solution: {target_solution_id}")
            return target_solution_id

        target_fact_id = self.kb.random_element(target_fact_range)
        self.question(target_fact_id)
        return None


if __name__ == '__main__':
    testTask = Task(KnowledgeBase('KnowledgeBase.db'))
    testTask.accepted_facts = [1]
    print(testTask._most_popular_solution())
    # while not testTask.find_solution_step():
    #     pass
