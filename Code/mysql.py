# 导入pymysql模块
import pymysql

# 我们这里需要多一步选择数据库
db = pymysql.connect(
    host='localhost',  # 这里输入主机名称一般来说都是localhost
    user='root',  # 这里输入mysql用户名
    password='123456',  # 这里输入密码
    port=3306,  # 这里输入端口号
    charset='utf8mb4',
    database='mysql'  # 这里选择数据库
)

# 创建一个游标对象
cursor = db.cursor()

# 创建一个名为 user 的表
table_name = "My_user"
# sql = 'show tables;'.format(table_name)
# # sql = 'create table {} (id varchar(20) not null, name varchar(20) not null, primary key(id))'.format(table_name)
# cursor.execute(sql)

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
