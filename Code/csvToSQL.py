import os

import mysql.connector  # pip install mysql-connector-python
import pandas as pd  # 导入pandas库，用于读取Excel文件和处理数据

from MySQLInfo import *

'''
2024/7/10
    insert_excel_data_to_mysql() //将csv表中的数据上传到云数据库/数据库
by陈邱华
'''

'''
path: 

'''


def excelToCsv(excelFilePath, sheetName, csvFilePath):
    # 读取excel文件
    df = pd.read_excel(excelFilePath)
    print(df)
    # 将数据保存为csv文件
    df.to_csv(csvFilePath, index=False)
    return True


def formationCheckAndInputToMySQL(path, sheetName=None, outputPath=None):
    try:
        fileExtension = os.path.splitext(path)[1].lower()
        csvFilePath = r"tempPath.csv"
        # 如果是excel文件
        if fileExtension in ['.xls', '.xlsx']:
            # 转化为csv文件
            excelToCsv(path, sheetName, csvFilePath)
            if insert_ranked_grades_to_mysql(csvFilePath):
                try:
                    os.remove("tempPath.csv")
                except FileNotFoundError:
                    print(f"文件不存在\n\n")
                return True
            return False
        elif fileExtension == '.csv':
            return insert_ranked_grades_to_mysql(path)
        else:
            return False
    except Exception as e:
        return False


def insert_ranked_grades_to_mysql(path, host=host, user=user, password=password, database=database,
                                  table=rankedGradesTable):
    """
    :param path: csv文件路径
    :param host: 数据库主机地址
    :param user: 数据库用户名
    :param password: 数据库密码
    :param database: 数据库名称
    :param table: 数据表名称
    :return:
    """
    # 连接数据库
    global mydb, sql
    try:
        mydb = mysql.connector.connect(
            host=host,  # 数据库主机地址
            user=user,  # 数据库用户名
            password=password,  # 数据库密码
            database=database  # 数据库名称
        )
    except Exception as e:
        print('无法连接至数据库{}'.format(database), e)
        mydb.rollback()
        mydb.close()
        return False

    #
    # 创建一个游标对象
    mycursor = mydb.cursor()

    # 读取CSV文件到DataFrame
    df = pd.read_csv(path)

    for index, row in df.iterrows():  # 遍历DataFrame中的每一行
        subjectList = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理']
        totalScore = 0
        for i in range(9):
            score = row[subjectList[i]]
            totalScore += score if score != -1 else 0
        # totalScore = row['语文'] + row['数学'] + row['英语'] + row['物理'] + row['化学'] + row['生物'] + row['历史'] + \
        #              row['政治'] + row['地理']
        data = f"'{row['姓名']}',{row['学号']},{row['语文']},{row['数学']},{row['英语']},{row['物理']},{row['化学']},{row['生物']},{row['历史']},{row['政治']},{row['地理']},{totalScore}"
        sql = (f"INSERT IGNORE INTO {table} "
               f"(姓名,学号,语文,数学,英语,物理,化学,生物,历史,政治,地理,总分) "
               f"VALUES ({data});")
        # # SQL插入语句
        print("正在插入数据至{}:".format(table), data)  # 输出正在插入的数据
        try:
            mycursor.execute(sql)  # 执行SQL插入语句
        except Exception as e:
            print('执行sql语句{}时错误'.format(sql), e)
            mydb.rollback()
            mycursor.close()
            mydb.close()

            return False

    # # 提交更改并关闭数据库连接
    mydb.commit()  # 提交更改
    mycursor.close()  # 关闭游标对象
    mydb.close()  # 关闭数据库连接
    return True

# path = './excelFiles/rankedCSV.csv'  # Excel文件路径
# host = "mysql.sqlpub.com"  # 数据库主机地址
# user = "orangeisland66"  # 数据库用户名
# password = "HM1620kJfibETKIE"  # 数据库密码
# database = "orangeisland66"  # 数据库名称
# table = "rankedGrades"  # 数据库表名
# insert_excel_data_to_mysql(path, host, user, password, database, table)  # 调用函数，将Excel数据插入到MySQL数据库中
