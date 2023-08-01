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


def display_hello_world(engine: Engine):
    with engine.connect() as conn:
        result: CursorResult = conn.execute(text("select 'hello world'"))
        print(type(result))
        rows = result.all()
        print(type(rows))
        print(rows)
        row: Row = rows[0]  # sqlalchemy.engine.row.Row
        # print(type(row))
        print(row)
        txt: str = row[0]
        # print(type(txt))
        print(txt)


def commit_as_you_go(engine: Engine):
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        result: CursorResult = conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()


def use_transaction_to_commit(engine: Engine):
    """"Assumes commit_as_you_go has been called previously"""
    with engine.begin() as conn:
        result: CursorResult = conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )


if __name__ == "__main__":
    print(f"python version: {get_python_version()}")
    print(f"SQLAlchemy version: {get_sqlalchemy_version()}")

    engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    # print(type(engine))

    display_hello_world(engine)
    commit_as_you_go(engine)
    use_transaction_to_commit(engine)
