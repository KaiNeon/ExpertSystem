import logging
from task_module import Task
from kb_module import KnowledgeBase
from db_module import DataBase

logging.basicConfig(level=logging.WARNING)


def print_solutions(kb, solutions):
    """Процедура вывода ответов в удобной форме"""
    print("\nВозможные решения:")
    solutions_verbal = kb.get_verbal('solutions', solutions)
    if not solutions:
        print(f"\tНет данных.")
    else:
        print(f"\tНомер\tНаименование\tИнформация")
        for row in solutions_verbal:
            print(f"\t{row[0]}\t\t{row[1]}\t\t{row[2]}")


# Точка входа основной программы
if __name__ == '__main__':
    data_base = DataBase("KnowledgeBase.db")
    knowledge_base = KnowledgeBase(data_base)
    testTask = Task(knowledge_base)
    while not testTask.find_solution_step():
        pass
    print_solutions(knowledge_base, testTask.get_answer())
