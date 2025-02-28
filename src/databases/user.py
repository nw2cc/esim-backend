import datetime

from amiyahttp import pwd_context
from src.databases import *

db = connect_database('esim')


class BaseModel(ModelClass):
    class Meta:
        database = db


class TableRows(BaseModel):
    remark = CharField(null=True)
    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())


@table
class Roles(TableRows):
    role_name = CharField(unique=True)
    is_admin = IntegerField(default=0)
    permissions = TextField(null=True)


@table
class Users(TableRows):
    role_id: Roles = ForeignKeyField(Roles, db_column='role_id', on_delete='SET NULL', null=True)
    username = CharField(unique=True)
    password = CharField()


def create_admin_user():
    Users.create(
        role_id=Roles.create(role_name='超级管理员', is_admin=1),
        username='admin',
        password=pwd_context.hash('admin8888'),
    )


async def get_user(username: str):
    user = Users.get_or_none(username=username)
    if user:
        return user.password
