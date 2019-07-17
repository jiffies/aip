import functools
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/aip?charset=utf8', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    from models import Plan, Record, Strategy
    Base.metadata.create_all(bind=engine)

@contextmanager
def DBSession():
    try:
        session = db_session()
        yield session
        print("session commit")
        session.commit()
    except SQLAlchemyError as e:
        db_session().rollback()
        raise e


