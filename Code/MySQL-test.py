#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas openpyxl sqlalchemy
# #pip install -i https://pypi.tuna.tsinghua.edu.cn/simple mysql-connector-python
# import pandas as pd
# from sqlalchemy import create_engine
#
# # 读取Excel文件
# excel_file = 'Grades.xlsx'
# sheet_name = 'Sheet1' # 如果你的Excel文件有多个工作表，更改这里的名称
# df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
#
# # 连接到MySQL数据库
# db_connection_str = 'mysql+mysqlconnector://username:password@host:port/database'
# db_connection = create_engine(db_connection_str)
#
# # 将DataFrame写入SQL表
# table_name = 'your_table_name' # 更改为你想要的表名
# df.to_sql(table_name, db_connection, if_exists='replace', index=False)
#
# print("Data imported to MySQL successfully!")
# 替换上述代码中的your_excel_file.xlsx、Sheet1、username、password、host、port、database和your_table_name为实际值



# 后续若要对数据库内容进行增删改查
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql
from pymysql import Connection
con=Connection(
    host='localhost',
    port=3306,
    user='root',
    password='865486'
) # 构建链接对象

# 非查询性质
cursor=con.cursor() #获取游标对象

con.select_db("mbb") # 选择数据库
#excute中的语句即SQL语句，需自学
cursor.execute("create table teacher(id int,name varchar(10),age int);") # 执行SQL语句
# 将代码使用多次换行时最好使用“三引号”，比如:
# sql="""
#     create table teacher(
#         id int,
#         name varchar(10),
#         age int
#     );
#     """
#cursor.execute(sql)

# 使用fetchone()获取一条结果
# fetchmany(n)获取n条结果
# fetchall()获取所有结果
# data=cursor.fetchone()
# print(data)

# 查询性质
# cursor=con.cursor() #获取游标对象
# con.select_db("sys") # 选择数据库
# cursor.execute("select * from student")
# results:tuple=cursor.fetchall()
# for x in results:
#     print(x)

# 插入数据
# cursor=con.cursor() #获取游标对象
# con.select_db("sys") # 选择数据库
#cursor.execute("insert into teacher values(1,'lf',88);")
#con.commit() # 插入数据要通过commit确认
# 或者在构建链接对象时，设置自动commit的属性：autocommit=True
# 在进行增，删，改时一定要使用con.commit()提交事务
con.close() # 关闭连接


#下面是简单的sql语法
"""
SQL的语言特征:
1、大小写不敏感
2、可以单行或多行书写，最后以;号结束
3、支持注释：
   单行注释：--注释内容（--后面一定要有一个空格）
   单行注释：#注释内容
   多行注释：/*注释内容*/
"""

"""
DDL-库管理：
查看所有数据库:show databases;
查询当前数据库：select database()
使用数据库:use 数据库名称;
创建数据库:create database [if not exists] 数据库名称 [default charset utf8][collate 排序规则];
删除数据库:drop database [if not exists] 数据库名称;

DDL-表管理：
查看表:show tables;
查询表结构:desc 表名;
查询指定表的建表语句:show create table 表名;
删除表:drop table 表名称;
      drop table if exists 表名称;
#[]括号中数据可省略
创建表:create table 表名称（
        列名称 列类型[comment '列注释']，
        列名称 列类型[comment '列注释']，
        .....
        ）[comment '表注释'];
修改表:
  添加字段:alter table 表名 add 字段名 类型(长度) [comment '注释'][约束];
  修改数据类型:alter table 表名 modify 字段名 新数据类型(长度);
  修改字段名和字段类型:alter table 表名 change 旧字段名 新字段名 类型(长度) [comment '注释'][约束];
  删除字段:alter table 表名 drop 字段名;
  修改表名:alter table 旧表名 rename to 新表名;
列表类型:tinyint (unsigned)--小整数值
        smallint (unsigned)--大整数值
        mediumint (unsigned)--大整数值
        int (unsigned)--整数
        bigint (unsigned)--极大整数值
        float (unsigned)--单精度浮点数
        double (unsigned)--双精度浮点数：double(a,b) a代表整数长度，b代表小数长度
        char(定*长度）--文本，长度为数字
        varchar（变*长度）--文本，长度为数字，做最大长度限制(输入的时候用单引号，如‘mbb’）
        data--日期类型
        time--时间值或持续时间
        datetime--混合日期和时间值
        timestamp--混合日期和时间值，时间戳类型
"""

"""
DML(数据操作语言):
#[]括号中数据可省略
数据插入:
  给指定列添加数据:insert into 表名(列1，列2，...) values(值1，值2，...，值N)
  给全部列添加数据:insert into 表名 values(值1，值2，...，值N)
  批量添加数据：insert into 表[(列1，列2，...,列N)] values(值1，值2，...，值N),(值1，值2，...，值N),....,(值1，值2，...，值N)
数据删除:delete from 表名称 [where 条件判断];   # =,<,>,<=,>=,!=
数据更新:update 表名称 set 列1=值1[,列2=值2,...] [where 条件判断];
"""

"""
where的条件判断:
     比较运算符:>,<,>=,<=,!=,between...and..[在某个范围内，包括最大值和最小值],
              in(...)[在in之后的列表中的值，多选一],like 占位符,is null[是NULL]
     逻辑运算符:and或&&,or或||,not或!
"""

"""
DQL:
数据查询：
   基本查询:select 列1,列2,.../* from 表 [where 条件判断];     #从表中选择某些列进行展示，/代表或者，*代表所有列
   设置别名: select 列1 [as 别名1],列2 [as 别名2],... from 表名;
   去除重复记录:select distinct 字段列表 from 表名;
   条件查询:select 字段列表 from 表名 where 条件判断;
分组聚合：select 字段1,字段2,.../聚合函数 from 表 [where 条件] group by 列;  # /代表或者
聚合函数：sum（列）--求和
        avg（列）--求平均值
        min（列）--求最小值
        max（列）--求最大值
        count（列|*）--求数量
        语法:select 聚合函数(字段列表) from 表名;
结果排序(可以对查询的结果使用order by关键字，指定某个列进行排序)：select 列|聚合函数|* from 表
        where...
        group by 分组字段名;
        order by 列1 排序方式1,列2 排序方式2...;
        # asc--升序；desc--降序
结果分页限制：select 字段列表 from 表名 limit 起始索引,查询记录数; (起始索引从0开始;起始索引=（查询页码-1）*每页记录数;如果查询的是第一页，只要写查询记录数)
"""

"""
DCL(数据控制语言):
创建用户：create user 用户名@主机名 identified by '密码';
删除用户：drop user 用户名@主机名;
修改用户：alter user 用户名@主机名 identified by '新密码';
查看权限：show grants for '用户名'@'主机名';
授权：grant 权限 on 数据库名.表名 to '用户名'@'主机名';
      grant 权限 on 数据库名.* to '用户名'@'主机名';
      grant 权限 on *.* to '用户名'@'主机名';
      grant 权限 on 数据库名.表名 to '用户名'@'主机名'; identified by '新密码';
撤销权限：revoke 权限 on 数据库名.表名 from '用户名'@'主机名';
"""