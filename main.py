import logging
from textwrap import wrap
from task_module import Task
from kb_module import KnowledgeBase
from db_module import DataBase

logging.basicConfig(level=logging.WARNING)


def justify(line, width):
    gap_width, max_replace = divmod(width - len(line) + line.count(' '), line.count(' '))
    return line.replace(' ', ' ' * gap_width).replace(' ' * gap_width, ' ' * (gap_width + 1), max_replace)


def lines_formatter(text, width, tabs):
    lines = wrap(text, width, break_long_words=False)
    for i, line in enumerate(lines[:-1]):
        if len(line) <= width and line.count(' '):
            lines[i] = justify(line, width).rstrip()
    return f"\n{tabs}".join(lines)


def print_solutions(kb: KnowledgeBase, solutions):
    """Процедура вывода ответов в читаемой форме"""
    print("\nВозможные решения:\n")
    solutions_verbal = kb.get_verbal('solutions', solutions)
    if not solutions:
        print(f"\tНет данных.")
    else:
        for row in solutions_verbal:
            information = lines_formatter(row[2], 60, '\t\t')
            print(f"\tНомер:\t{row[0]}\n"
                  f"\tПроблема:\t{row[1]}\n"
                  f"\tРешение:\n\t\t{information}\n")


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
