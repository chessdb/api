import datetime
from typing import List, Tuple

import pydantic

from chessdb_api.core.db import DB
from chessdb_api.domain.positions import position_model, position_schemas

CreateSchema = position_schemas.Create
UpdateSchema = position_schemas.Update
Model = position_model.Model


class Queries():

    async def create(self, position: CreateSchema) -> Model:
        return await Model.create(**position.__dict__)

    async def get_list(self, page_size: int,
                       page: int) -> Tuple[List[Model], int]:
        positions: List[Model] = await Model.query.order_by(
            Model.fen.asc()).offset(page_size * (page - 1)
                                   ).limit(page_size).gino.all()

        count = await DB.func.count(Model.identifier).gino.scalar()
        return positions, count

    async def get_by_id(self, identifier: pydantic.UUID4) -> Model:
        return await Model.get(identifier)

    async def delete(self, identifier: pydantic.UUID4) -> Model:
        position = await self.get_by_id(identifier)
        await position.delete()
        return position

    async def update(self, old_position: Model,
                     new_position: UpdateSchema) -> Model:
        updated_position = await old_position.update(**new_position.__dict__
                                                    ).apply()
        return updated_position._instance
