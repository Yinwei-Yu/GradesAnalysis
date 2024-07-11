import mysql.connector  # pip install mysql-connector-python
import pandas as pd  # 导入pandas库，用于读取Excel文件和处理数据

'''
2024/7/10
    insert_excel_data_to_mysql() //将csv表中的数据上传到云数据库/数据库
by陈邱华
'''

'''
path: 

'''
from mysql1 import createTable


def insert_excel_data_to_mysql(path, host, user, password, database, table):
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
    global mydb
    try:
        mydb = mysql.connector.connect(
            host=host,  # 数据库主机地址
            user=user,  # 数据库用户名
            password=password,  # 数据库密码
            database=database  # 数据库名称
        )
    except Exception as e:
        print('无法连接至数据库{}'.format(database), e)
        mydb.close()

    #
    # 创建一个游标对象
    mycursor = mydb.cursor()

    # 读取CSV文件到DataFrame
    df = pd.read_csv(path)
    # df.fillna(0)

    #
    # # 将DataFrame写入MySQL表
    # # 假设CSV的列名与MySQL表的列名匹配
    # df.to_sql(table, mydb, if_exists='replace', index=False)
    #
    # # 步骤5: 关闭游标和连接
    # cursor.close()
    # mydb.close()
    # # 将日期时间类型的列转换为字符串类型
    # for col in df.columns:  # 遍历DataFrame中的每一列
    #     if df[col].dtype == 'datetime64[ns]':  # 如果该列的数据类型是日期时间类型
    #         df[col] = df[col].astype(str)  # 将该列的数据类型转换为字符串类型
    # 先清空表格
    sql = 'TRUNCATE TABLE {};'.format(table)
    # mycursor.execute(sql)
    try:
        mycursor.execute(sql)
    except mysql.connector.errors.ProgrammingError as e:

        print("表格还未创建，正在创建表格……", e)
        createTable(table, host, user, password, 3306, 'utf8mb4', database=database)

    mycursor.close()
    mycursor = mydb.cursor()
    # 遍历Excel表格中的每一行，并将每一行插入到数据库中
    for row in df.itertuples(index=False):  # 遍历DataFrame中的每一行
        sql = (f"INSERT INTO {table} "
               f"(姓名,学号,语文,数学,英语,物理,化学,生物,历史,政治,地理,总分) "
               f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")
        # # SQL插入语句
        val = row  # 插入的数据
        print("正在插入数据:", val)  # 输出正在插入的数据
        try:
            mycursor.execute(sql, val)  # 执行SQL插入语句
        except Exception as e:
            print('执行sql语句{}时错误'.format(sql), e)
            mydb.close()
            mycursor.close()

    # # 提交更改并关闭数据库连接
    mydb.commit()  # 提交更改
    mycursor.close()  # 关闭游标对象
    mydb.close()  # 关闭数据库连接

path = './excelFiles/rankedCSV.csv'  # Excel文件路径
host = "mysql.sqlpub.com"  # 数据库主机地址
user = "orangeisland66"  # 数据库用户名
password = "HM1620kJfibETKIE"  # 数据库密码
database = "orangeisland66"  # 数据库名称
table = "rankedGrades"  # 数据库表名
insert_excel_data_to_mysql(path, host, user, password, database, table)  # 调用函数，将Excel数据插入到MySQL数据库中
