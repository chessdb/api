from typing import List, Optional

import pydantic

from chessdb_api.domain import base_schemas
from chessdb_api.domain.positions import position_queries, position_schemas


class Service:
    """Service.
    """

    def __init__(self, queries: position_queries.Queries):
        self._queries = queries

    async def create(self,
                     position: position_schemas.Create) -> position_schemas.DB:
        new_position = await self._queries.create(position=position)
        return position_schemas.DB.from_orm(new_position)

    async def get_by_id(self, fen: pydantic.UUID4) -> position_schemas.DB:
        position = await self._queries.get_by_id(fen=fen)
        if position:
            return position_schemas.DB.from_orm(position)
        return None

    async def get_list(
        self,
        page: pydantic.conint(ge=1),
        page_size: pydantic.conint(ge=1, le=100),
    ) -> position_schemas.Paginated:
        positions, total = await self._queries.get_list(page=page,
                                                        page_size=page_size)
        more = ((total / page_size) - page) > 0
        results = [
            position_schemas.DB.from_orm(position) for position in positions
        ]
        pagination = base_schemas.Pagination(total=total, more=more)
        return position_schemas.Paginated(results=results,
                                          pagination=pagination)

    async def update(
            self, fen: pydantic.UUID4,
            new_position: position_schemas.Update) -> position_schemas.DB:
        old_position = await self._queries.get_by_id(fen=fen)
        updated_position = await self._queries.update(old_position=old_position,
                                                      new_position=new_position)
        return position_schemas.DB.from_orm(updated_position)

    async def delete(self, fen: pydantic.UUID4) -> position_schemas.DB:
        deleted_position = await self._queries.delete(fen=fen)
        return position_schemas.DB.from_orm(deleted_position)
