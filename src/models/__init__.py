from pydantic import BaseModel


class PageQuery(BaseModel):
    pageNum: int
    pageSize: int


class ById(BaseModel):
    id: int
