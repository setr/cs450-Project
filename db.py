import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
from collections import namedtuple
import pymysql

#engine = sqlalchemy.create_engine('mysql+pymysql://root:password@cs425.cdm3zyogivv9.us-west-2.rds.amazonaws.com:3306/library')
connection = pymysql.connect(
    user='root',
    password='password',
    host='cs425.cdm3zyogivv9.us-west-2.rds.amazonaws.com',
    port=3306,
    db='library',
    cursorclass=pymysql.cursors.DictCursor)

def select(query, data, many):
    result = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, data)
            if many:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
    finally:
        pass
    return result
    #finally:
    #    connection.close()

def CUD(queries, datas):
    try:
        with connection.cursor() as cursor:
            for query, data in zip(queries, datas):
                cursor.execute(query, data)
        connection.commit()
    finally:
        connection.close()

def getAllSecurity():
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    result = s.execute('SELECT * FROM Security').fetchall()
    return result

def login(user, passw):
    #q = "SELECT username, levelname from Account join Security on Account.SecurityLevel = Security.SecurityLevel where username = %s and password = %s"
    q = "call sp_credcheck(%s,%s)"
    print q % (user, passw)
    result = select(query=q, data=(user, passw), many=False)
    print result
    return result
            
    #Session = scoped_session(sessionmaker(bind=engine))
    #s = Session()
    #q = text("SELECT username, levelname from Account join Security on Account.SecurityLevel = Security.SecurityLevel where username = :user and password = :passw")
    #result = s.execute(q.bindparams(user=user, passw=passw)).fetchone()
    #return result

    #result = s.execute(q.bindparams(user=user, passw=passw)).fetchone()
print login('keshav', '1211')
#getAllSecurity()
