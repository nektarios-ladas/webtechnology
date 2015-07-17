import pymysql

def openDatabase():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology')
    return conn

def closeDatabase(conn):
    conn.close()
