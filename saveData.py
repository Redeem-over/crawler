import pymysql
host = 'localhost'
database = 'xiecheng'
password = 'root'
user = 'qwert12345'
port = 3306
def  save2Mysql(item,table):
    db = pymysql.connect(host=host,user=user,password=password,port=port,db=database)
    cursor = db.cursor()
    keys =','.join(item.keys())
    values = ','.join(['% s'] * len(item))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(item.values())):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()