from fastapi import Query


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Número de página"),
        size: int = Query(20, ge=1, le=100, description="Elementos por página"),
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size
        self.limit = size
