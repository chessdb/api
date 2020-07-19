"""Helps execute SQL migrations inside .sql files.

"""
import pathlib

from sqlalchemy import orm


def execute(bind, filename: str):
    """executes raw sql inside a .SQL file

    upgrade.sql or downgrade.sql inside a migrations folder is the typical
    filename.

    Args:
        bind:
        filename (str): filename
    """
    session = orm.Session(bind=bind)
    file_path = pathlib.Path(f"migrations/versions/{filename}").absolute()
    with open(file_path) as f:
        sql_to_execute = f.read()
        session.execute(sql_to_execute)
        session.commit()
