from peewee import *

from models import *

# config - aside from our database, the rest is for use by Flask
DATABASE = 'infra/base.db'
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'


# create a peewee database instance -- our models will use this database to
# persist information
# db = SqliteDatabase(DATABASE)

sqlite_1 = SqliteDatabase(DATABASE)
# sqlite_2 = pw.PostgresqlDatabase('sqlite_2.db')

db.initialize(sqlite_1)


def create_tables_increment():
    with db:
        db.create_tables([Pessoa])

# simple utility function to create tables


def create_tables():
    with db:
        db.create_tables([User, Questionario, Pergunta,
                          Resposta, Grupo, Dimensao,])


create_tables_increment()
