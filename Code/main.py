# 待实现
from multiprocessing import Manager

from AccountManager import *
from GradeManager import *
from Login_Window import *


gradeManager = GradeManager([], 0, [], 0)
gradeManager.inputMore("./excelFiles/student_grades.xls")
accountManager = AccountManager()
if __name__ == "__main__":

    mgr = Manager()
    shared_list = mgr.list()
    #freeze_support()
    start()
