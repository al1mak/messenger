from db.db_lib import Storage
from db import Client, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Test:

    def __init__(self):

        engine = create_engine('sqlite:///:memory:', echo=False)
        # Не забываем создать структуру базы данных
        Base.metadata.create_all(engine)
        # Создаем сессию для работы
        Session = sessionmaker(bind=engine)
        session = Session()
        # Рекомендуется брать 1 сессию и передавать параметром куда нам надо
        self.session = session
        # далее создаем тестовые

        client = Client('Vasya')
        self.session.add(client)

        self.repo = Storage(session)

    # def test(self):
    #
    #     engine = create_engine('sqlite:///:memory:', echo=False)
    #     # Не забываем создать структуру базы данных
    #     Base.metadata.create_all(engine)
    #     # Создаем сессию для работы
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     # Рекомендуется брать 1 сессию и передавать параметром куда нам надо
    #     self.session = session
    #     # далее создаем тестовые
    #
    #     client = Client('Vasya')
    #     self.session.add(client)
    #
    #     self.repo = Storage(session)

    def test_add_client(self):

        self.repo.add_client('New Ivan')

    def test_get_client(self, name):

        client = self.repo.get_client(name)
        return client




test = Test()

test.test_add_client()
print(test.test_get_client('Vasya'))