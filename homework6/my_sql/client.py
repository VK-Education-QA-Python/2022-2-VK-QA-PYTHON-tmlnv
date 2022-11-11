import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.tasks import Base


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url, connect_args={'autocommit': True})
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def delete_db(self):
        # self.connect(db_created=True)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')

    def create_table_task1(self):
        if not sqlalchemy.inspect(self.engine).has_table('task1'):
            Base.metadata.tables['task1'].create(self.engine)

    def create_table_task2(self):
        if not sqlalchemy.inspect(self.engine).has_table('task2'):
            Base.metadata.tables['task2'].create(self.engine)

    def create_table_task3(self):
        if not sqlalchemy.inspect(self.engine).has_table('task3'):
            Base.metadata.tables['task3'].create(self.engine)

    def create_table_task4(self):
        if not sqlalchemy.inspect(self.engine).has_table('task4'):
            Base.metadata.tables['task4'].create(self.engine)

    def create_table_task5(self):
        if not sqlalchemy.inspect(self.engine).has_table('task5'):
            Base.metadata.tables['task5'].create(self.engine)

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
