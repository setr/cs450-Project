import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session


engine = sqlalchemy.create_engine('mysql+pymysql://root:password@cs425.cdm3zyogivv9.us-west-2.rds.amazonaws.com:3306/library')

def getAllSecurity():
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    result = s.execute('SELECT * FROM Security').fetchall()
    print result
    return result

getAllSecurity()
