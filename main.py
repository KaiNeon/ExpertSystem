import logging
from task_module import Task
from kb_module import KnowledgeBase
from db_module import DataBase

logging.basicConfig(level=logging.WARNING)


def line_format(line, words):
    buff_line = line.split()
    result = []
    for i in range(0, len(buff_line), words):
        word_line = buff_line[i: i + words]
        if len(word_line[-1]) > words:
            result.append(" ".join(word_line[:-1]))
            result.append(word_line[-1])
        else:
            result.append(" ".join(word_line))
    return result


def print_solutions(kb: KnowledgeBase, solutions):
    """Процедура вывода ответов в читаемой форме"""
    tabs = '\t'
    print("\nВозможные решения:")
    solutions_verbal = kb.get_verbal('solutions', solutions)
    if not solutions:
        print(f"{tabs}Нет данных.")
    else:
        for row in solutions_verbal:
            information = f"\n{tabs}\t".join(line_format(row[2], 15))
            print(f"\n{tabs}Номер:\t{row[0]}\n"
                  f"{tabs}Проблема:\t{row[1]}\n"
                  f"{tabs}Решение:\n{tabs}\t{information}")


def print_voting(task: Task, solutions):
    """Процедура проведения опроса"""
    solutions_str = [str(solution) for solution in solutions]
    answer = "blank"
    while answer not in solutions_str and answer:
        answer = input("\nВведите номер верного решения или пустую строку.\n")
    if answer:
        task.set_votes(solutions)


# Точка входа основной программы
if __name__ == '__main__':
    data_base = DataBase("KnowledgeBase_rev.db")
    knowledge_base = KnowledgeBase(data_base)
    testTask = Task(knowledge_base)
    while not testTask.find_solution_step():
        pass
    possible_solutions = testTask.get_answer()
    print_solutions(knowledge_base, possible_solutions)
    print_voting(testTask, possible_solutions)
