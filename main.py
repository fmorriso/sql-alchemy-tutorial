"""
https://docs.sqlalchemy.org/en/20/tutorial/engine.html
"""

import sys

import sqlalchemy
from sqlalchemy import create_engine, Engine, text, CursorResult, Row


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_sqlalchemy_version() -> str:
    return sqlalchemy.__version__


if __name__ == "__main__":
    print(f"python version: {get_python_version()}")
    print(f"SQLAlchemy version: {get_sqlalchemy_version()}")

    engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    # print(type(engine))

    with engine.connect() as conn:
        result: CursorResult = conn.execute(text("select 'hello world'"))
        print(type(result))
        rows = result.all()
        print(type(rows))
        print(rows)
        row: Row = rows[0] # sqlalchemy.engine.row.Row
        # print(type(row))
        print(row)
        txt: str = row[0]
        # print(type(txt))
        print(txt)
