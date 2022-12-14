import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '0.0.0.0'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self):
        db = self.db_name
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url, connect_args={'autocommit': True})
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def insert_query(self, name, surname, middle_name, username, password, email):
        self.execute_query(
            f"""INSERT INTO test_users (name, surname, middle_name, username, password, email, access)
             VALUES ('{name}', '{surname}', '{middle_name}', '{username}', '{password}', '{email}', 1);""")
