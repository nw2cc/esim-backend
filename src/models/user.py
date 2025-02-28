from typing import Optional
from src.models import PageQuery, BaseModel


class UserQuery(PageQuery): ...


class UserModel(BaseModel):
    id: Optional[int]
    role_id: int
    username: str
    remark: str = ''
