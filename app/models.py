from peewee import *
DATABASE = "test"
HOST = "db"
USER = "root"
PASSWORD = "example"

db = MySQLDatabase(  
    database=DATABASE,
    host=HOST,
    user=USER,
    password=PASSWORD
    )
class Base(Model):
    class Meta:
        database=db

class User(Base):
    firstname = CharField()
    lastname = CharField()
    phone = CharField()
    email = CharField()
    password_=TextField()
    class Meta:
        db_table='users' 

class Task(Base):
    task = TextField()
    user = ForeignKeyField(User, backref='tasks')
    class Meta:
        db_table='tasks'

db.connect()
db.create_tables([User, Task])






