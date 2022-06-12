import logging
from task_module import Task
from kb_module import KnowledgeBase
from db_module import DataBase

logging.basicConfig(level=logging.INFO)


def print_solutions(kb, solutions):
    print("Возможные решения:")
    solutions_verbal = kb.get_verbal('solutions', solutions)
    for row in solutions_verbal:
        print(f"\t{row[0]})\t{row[1]}:\t{row[2]}")


if __name__ == '__main__':
    data_base = DataBase("KnowledgeBase.db")
    knowledge_base = KnowledgeBase(data_base)
    testTask = Task(knowledge_base)
    while not testTask.find_solution_step():
        pass
    print_solutions(knowledge_base, testTask.get_answer())
