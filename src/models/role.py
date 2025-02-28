from typing import List, Optional
from src.models import PageQuery, BaseModel


class RoleQuery(PageQuery): ...


class RoleModel(BaseModel):
    id: Optional[int]
    role_name: str
    is_admin: bool
    permissions: List[str]
    remark: str = ''
