from sqlalchemy.orm import Query
from pydantic import BaseModel, Field
from typing import Generic, List, TypeVar, Type, Optional, Tuple
from sqlalchemy import asc, desc


T = TypeVar("T")


class PaginationInfo(BaseModel):
    page_num: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    total_rows: int
    total_pages: int


class Paginated(BaseModel, Generic[T]):
    pagination: PaginationInfo
    results: List[T]


class Paginator:
    def __init__(
        self,
        model_class: Type,
        page_num: int = 1,
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ):
        self.page_num = page_num
        self.page_size = page_size
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.model_class = model_class

    def apply(self, query: Query) -> Tuple[Query, PaginationInfo]:
        if self.sort_by and hasattr(self.model_class, self.sort_by):
            field = getattr(self.model_class, self.sort_by)
            query = query.order_by(asc(field) if self.sort_order == "asc" else desc(field))

        total_rows = query.count()
        total_pages = (total_rows + self.page_size - 1) // self.page_size
        paginated = query.offset((self.page_num - 1) * self.page_size).limit(self.page_size)

        return paginated, PaginationInfo(
            page_num=self.page_num,
            page_size=self.page_size,
            total_rows=total_rows,
            total_pages=total_pages
        )
