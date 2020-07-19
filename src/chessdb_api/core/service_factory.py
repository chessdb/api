from chessdb_api.domain.positions import position_queries, position_services


def get_position_services() -> position_services.Service:
    return position_services.Service(position_queries.Queries())
