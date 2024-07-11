# 导入pymysql模块
import pymysql

'''
2024/7/11：
    createTable该模块实现在MySQL数据库中创建表
by陈邱华
'''


def createTable(table_name, host, user, password, port, charset, database):
    # 我们这里需要多一步选择数据库
    print(port)
    db = pymysql.connect(host=host, user=user, password=password, port=port, charset=charset, database=database)

    # 创建一个游标对象
    cursor = db.cursor()
    # 姓名,学号,语文,数学,英语,物理,化学,生物,历史,政治,地理,总分
    # 创建表
    # sql = 'drop table {};'.format(table_name)
    # cursor.execute(sql)
    # sql = ('create table {} (姓名 varchar(20) not null, 学号 varchar(20) not null, '
    #        '语文 varchar(20) not null,数学 varchar(20) not null)').format(
    #     table_name)
    sql = (f'create table {table_name} (姓名 varchar(20) not null, 学号 varchar(20) not null, 语文 varchar(20) not null,'
           f'数学 varchar(20) not null, 英语 varchar(20) not null, 物理 varchar(20) not null, 化学 varchar(20) not null,'
           f' 生物 varchar(20) not null, 历史 varchar(20) not null, 政治 varchar(20) not null, 地理 varchar(20) not null,'
           f' 总分 varchar(20) not null);')

    try:
        cursor.execute(sql)
    except Exception as e:
        print("执行失败！", e)
        cursor.close()

    # 把创建的表显示出来
    sql = 'show tables;'
    cursor.execute(sql)
    print("显示创建的表：", cursor.fetchall())

    # 显示表的结构
    sql = 'desc {}'.format(table_name)
    cursor.execute(sql)
    print("显示表的结构：", cursor.fetchall())

    cursor.close()
    db.close()  # 关闭数据库连接


# host = 'mysql.sqlpub.com'  # 这里输入主机名称一般来说都是localhost
# user = 'orangeisland66'  # 这里输入mysql用户名
# password = 'HM1620kJfibETKIE' # 这里输入密码
# port = 3306  # 这里输入端口号
# charset = 'utf8mb4'
# database = 'orangeisland66'  # 这里选择数据库
# table_name = 'rankedGrades'
# createTable(table_name, host, user, password, port, charset, database)
