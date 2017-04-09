import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
from collections import namedtuple


engine = sqlalchemy.create_engine('mysql+pymysql://root:password@cs425.cdm3zyogivv9.us-west-2.rds.amazonaws.com:3306/library')

def getAllSecurity():
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    result = s.execute('SELECT * FROM Security').fetchall()
    return result

def login(user, passw):
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    q = text("SELECT username, password, securitylevel from Account where username = :user and password = :passw")
    result = s.execute(q.bindparams(user=user, passw=passw)).fetchone()
    return result

print login('keshav', '1211')
#getAllSecurity()
