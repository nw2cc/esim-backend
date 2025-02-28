import datetime

from amiyahttp import authorized_user, pwd_context, HTTPException
from src import app
from src.databases import select_for_paginate
from src.databases.user import Users, create_admin_user
from src.models.user import UserQuery, UserModel
from src.models import ById


if not Users.get_or_none(username='admin'):
    try:
        create_admin_user()
    except Exception as e:
        ...


def format_user(item: dict) -> dict:
    item['role_name'] = item['role_id']['role_name']
    item['role_id'] = item['role_id']['id']
    return item


@app.controller
class User:
    @app.route(method='get')
    async def get_user_info(self, username: str = authorized_user()):
        user: Users = Users.get_or_none(username=username)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        return app.response(
            {
                'user': {
                    'admin': bool(user.role_id.is_admin),
                    'avatar': '',
                    'nick_name': username,
                    'user_name': username,
                },
                'permissions': (user.role_id.permissions or '').split(','),
            }
        )

    @app.route(method='post')
    async def create_user(self, params: UserModel, username: str = authorized_user()):
        exists = Users.get_or_none(username=params.username)
        if exists:
            return app.response(code=500, message='用户已存在')

        Users.create(
            role_id=params.role_id,
            username=params.username,
            password=pwd_context.hash('123456'),
            remark=params.remark,
        )
        return app.response(message='创建成功')

    @app.route(method='post')
    async def update_user(self, params: UserModel, username: str = authorized_user()):
        Users.update(
            role_id=params.role_id,
            username=params.username,
            remark=params.remark,
            update_time=datetime.datetime.now(),
        ).where(Users.id == params.id).execute()
        return app.response(message='修改成功')

    @app.route(method='post')
    async def delete_user(self, params: ById, username: str = authorized_user()):
        Users.delete().where(Users.id == params.id).execute()
        return app.response(message='删除成功')

    @app.route(method='post')
    async def get_user_page(self, params: UserQuery, username: str = authorized_user()):
        return app.response(
            select_for_paginate(
                Users.select(),
                params.pageNum,
                params.pageSize,
                item_format=format_user,
            )
        )
