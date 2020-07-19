"""Example Google style docstrings.

"""
from typing import List
from typing import Tuple

from chessdb_api.core.db import DB
from chessdb_api.domain.positions import position_model
from chessdb_api.domain.positions import position_schemas
import pydantic

CreateSchema = position_schemas.Create
UpdateSchema = position_schemas.Update
Model = position_model.Model


class Queries():
    """Queries.
    """

    async def create(self, position: CreateSchema) -> Model:
        """create.

        Args:
            position (CreateSchema): position

        Returns:
            Model:
        """
        return await Model.create(**position.__dict__)

    async def get_list(self, page_size: int,
                       page: int) -> Tuple[List[Model], int]:
        """get_list.

        Args:
            page_size (int): page_size
            page (int): page

        Returns:
            Tuple[List[Model], int]:
        """
        positions: List[Model] = await Model.query.order_by(
            Model.fen.asc()).offset(page_size * (page - 1)
                                   ).limit(page_size).gino.all()

        count = await DB.func.count(Model.fen).gino.scalar()
        return positions, count

    async def get_by_id(self, fen: pydantic.UUID4) -> Model:
        """get_by_id.

        Args:
            fen (pydantic.UUID4): fen

        Returns:
            Model:
        """
        return await Model.get(fen)

    async def delete(self, fen: pydantic.UUID4) -> Model:
        """delete.

        Args:
            fen (pydantic.UUID4): fen

        Returns:
            Model:
        """
        position = await self.get_by_id(fen)
        await position.delete()
        return position

    async def update(self, old_position: Model,
                     new_position: UpdateSchema) -> Model:
        """update.

        Args:
            old_position (Model): old_position
            new_position (UpdateSchema): new_position

        Returns:
            Model:
        """
        position = await old_position.update(**new_position.__dict__).apply()
        return position._instance
