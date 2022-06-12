import logging
from task_module import Task
from kb_module import KnowledgeBase
from db_module import DataBase

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    testTask = Task(KnowledgeBase(DataBase("KnowledgeBase.db")))
    while not testTask.find_solution_step():
        pass
