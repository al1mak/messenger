from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships, sessionmaker
import os

Base = declarative_base()


class Client(Base):

    __tablename__ = 'Client'
    ClientId = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)

    def __init__(self, name):
        self.Name = name

    def __repr__(self):
        return "<Client ('%s')>" % self.Name


class ClientContact(Base):

    __tablename__ = 'ClientContact'
    ClientContactId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))

    def __init__(self, client_id, contact_id):

        self.ClientId = client_id
        self.ContactId = contact_id


# DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# print(DB_FOLDER_PATH)
# DB_PATH = os.path.join(DB_FOLDER_PATH, 'server.db')
# engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=True)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session
#
# print(type(session))

# путь до папки где лежит этот модуль
DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь до файла базы данных
DB_PATH = os.path.join(DB_FOLDER_PATH, 'server.db')
#создаем движок
engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=False)
# Не забываем создать структуру базы данных
Base.metadata.create_all(engine)
# Создаем сессию для работы
Session = sessionmaker(bind=engine)
session = Session()
# Рекомендуется брать 1 сессию и передавать параметром куда нам надо
#session = session