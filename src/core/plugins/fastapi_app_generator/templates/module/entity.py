from pydantic import BaseModel
from typing import Optional, List


# Entity for {{ entity.name }}
class {{ entity.name }}(BaseModel):
    {% for column in entity.columns %}
    {{column.name}}: {{column.type}}
    {% endfor %}

    class Config:
        orm_mode = True


class {{ entity.name }}Create(BaseModel):
    {% for column in entity.columns if not column.primary_key %}
    {{column.name}}: {{column.type}}
    {% endfor %}

    class Config:
        orm_mode = True


class {{ entity.name }}Update(BaseModel):
    {% for column in entity.columns if not column.primary_key %}
    {{column.name}}: Optional[{{column.type}}] = None
    {% endfor %}

    class Config:
        orm_mode = True


class {{ entity.name }}List(BaseModel):
    items: List[{{entity.name}}]

    class Config:
        orm_mode = True

class {{ entity.name }}Response(BaseModel):
    item: {{entity.name}}

    class Config:
        orm_mode = True


class {{ entity.name }}Filter(BaseModel):
    {% for column in entity.columns %}
    {{column.name}}: Optional[{{column.type}}] = None
    {% endfor %}

    class Config:
        orm_mode = True

class {{ entity.name }}Pagination(BaseModel):
    items: List[{{entity.name}}]
    total: int
    page: int
    size: int

    class Config:
        orm_mode = True


class {{ entity.name }}Count(BaseModel):
    count: int

    class Config:
        orm_mode = True


class {{ entity.name }}Exists(BaseModel):
    exists: bool

    class Config:
        orm_mode = True


class {{ entity.name }}BulkCreate(BaseModel):
    items: List[{{entity.name}}Create]

    class Config:
        orm_mode = True


class {{ entity.name }}BulkUpdate(BaseModel):
    items: List[{{entity.name}}Update]

    class Config:
        orm_mode = True


class {{ entity.name }}BulkDelete(BaseModel):
    ids: List[int]

    class Config:
        orm_mode = True


class {{ entity.name }}BulkResponse(BaseModel):
    items: List[{{entity.name}}]

    class Config:
        orm_mode = True

