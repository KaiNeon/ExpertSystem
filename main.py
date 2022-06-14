import logging
from task_module import Task
from kb_module import KnowledgeBase
from db_module import DataBase

logging.basicConfig(level=logging.WARNING)


def print_solutions(kb: KnowledgeBase, solutions):
    """Процедура вывода ответов в читаемой форме"""
    print("\nВозможные решения:")
    solutions_verbal = kb.get_verbal('solutions', solutions)
    if not solutions:
        print(f"\tНет данных.")
    else:
        print(f"\tНомер\tНаименование\tИнформация")
        for row in solutions_verbal:
            print(f"\t{row[0]}\t\t{row[1]}\t\t{row[2]}")


def print_voting(task: Task, solutions):
    """Процедура проведения опроса"""
    answer = input("\nВведите не пустую строку, если решение оказалось верным.\n")
    if answer:
        task.set_votes(solutions)


# Точка входа основной программы
if __name__ == '__main__':
    data_base = DataBase("KnowledgeBase.db")
    knowledge_base = KnowledgeBase(data_base)
    testTask = Task(knowledge_base)
    while not testTask.find_solution_step():
        pass
    possible_solutions = testTask.get_answer()
    print_solutions(knowledge_base, possible_solutions)
    print_voting(testTask, possible_solutions)
