import datetime

from amiyahttp import authorized_user
from src import app
from src.databases import select_for_paginate, query_to_list
from src.databases.user import Roles
from src.models.role import RoleQuery, RoleModel
from src.models import ById


def format_role(item: dict) -> dict:
    item['is_admin'] = bool(item['is_admin'])
    item['permissions'] = (item['permissions'] or '').split(',')
    return item


@app.controller
class Role:
    @app.route(method='get')
    async def get_all_role(self, username: str = authorized_user()):
        return app.response(query_to_list(Roles.select()))

    @app.route(method='post')
    async def get_role_page(self, params: RoleQuery, username: str = authorized_user()):
        return app.response(
            select_for_paginate(
                Roles.select(),
                params.pageNum,
                params.pageSize,
                item_format=format_role,
            )
        )

    @app.route(method='post')
    async def create_role(self, params: RoleModel, username: str = authorized_user()):
        exists = Roles.get_or_none(role_name=params.role_name)
        if exists:
            return app.response(code=500, message='角色名已存在')

        Roles.create(
            role_name=params.role_name,
            is_admin=int(params.is_admin),
            permissions=','.join(params.permissions),
            remark=params.remark,
        )
        return app.response(message='创建成功')

    @app.route(method='post')
    async def update_role(self, params: RoleModel, username: str = authorized_user()):
        Roles.update(
            role_name=params.role_name,
            is_admin=int(params.is_admin),
            permissions=','.join(params.permissions),
            remark=params.remark,
            update_time=datetime.datetime.now(),
        ).where(Roles.id == params.id).execute()
        return app.response(message='修改成功')

    @app.route(method='post')
    async def delete_role(self, params: ById, username: str = authorized_user()):
        Roles.delete().where(Roles.id == params.id).execute()
        return app.response(message='删除成功')
