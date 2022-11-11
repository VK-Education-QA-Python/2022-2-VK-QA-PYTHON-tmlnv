from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR

Base = declarative_base()


class Task1Model(Base):

    __tablename__ = 'task1'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Task id={self.id}, total_number_of_requests={self.total_number_of_requests}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_number_of_requests = Column(Integer(), nullable=False)


class Task2Model(Base):

    __tablename__ = 'task2'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Task id={self.id}, method={self.method}, number_of_requests={self.number_of_requests}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(VARCHAR(100), nullable=False)
    number_of_requests = Column(Integer(), nullable=False)


class Task3Model(Base):

    __tablename__ = 'task3'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Task id={self.id}, url={self.url}, number_of_requests={self.number_of_requests}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(50), nullable=False)
    number_of_requests = Column(Integer(), nullable=False)


class Task4Model(Base):

    __tablename__ = 'task4'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Task id={self.id}, ip={self.ip}, url={self.url}, status_code={self.status_code}, request_size={self.request_size}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(100), nullable=False)
    url = Column(VARCHAR(500), nullable=False)
    status_code = Column(Integer(), nullable=False)
    request_size = Column(Integer(), nullable=False)


class Task5Model(Base):

    __tablename__ = 'task5'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Task id={self.id}, ip={self.ip}, number_of_requests={self.number_of_requests}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(100), nullable=False)
    number_of_requests = Column(Integer(), nullable=False)
