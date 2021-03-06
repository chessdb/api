from chessdb_api.core import service_factory
from chessdb_api.domain.positions import position_schemas
import fastapi
import pydantic
from starlette import status

router = fastapi.APIRouter()


@router.get("/", response_model=position_schemas.Paginated)
async def get_positions(page_size: pydantic.conint(ge=1, le=100) = 20,
                        page: pydantic.conint(ge=1) = 1,
                        service=fastapi.Depends(
                            service_factory.get_position_services)):
    return await service.get_list(page=page, page_size=page_size)


@router.post("/",
             response_model=position_schemas.DB,
             status_code=status.HTTP_201_CREATED)
async def add_position(position: position_schemas.Create,
                       service=fastapi.Depends(
                           service_factory.get_position_services)):
    return await service.create(position=position)


@router.put("/{fen}", response_model=position_schemas.DB)
async def update_position(fen: str,
                          position: position_schemas.Update,
                          service=fastapi.Depends(
                              service_factory.get_position_services)):
    position = await service.update(fen=fen, new_position=position)
    if position:
        return position
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A position with id: '{fen} was not found.",
    )


@router.get("/{fen}", response_model=position_schemas.DB)
async def get_position(fen: str,
                       service=fastapi.Depends(
                           service_factory.get_position_services)):
    position = await service.get_by_id(fen=fen)
    if position:
        return position
    raise fastapi.HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"A position with id: '{fen} was not found.",
    )


@router.delete("/{fen}", response_model=position_schemas.DB)
async def delete_position(fen: str,
                          service=fastapi.Depends(
                              service_factory.get_position_services)):
    return await service.delete(fen=fen)
