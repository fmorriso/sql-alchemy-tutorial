"""
https://docs.sqlalchemy.org/en/20/tutorial/index.html
"""
import inspect
import sys, inspect

import sqlalchemy
from sqlalchemy import (
    create_engine,
    Engine,
    text,
    CursorResult,
    Row,
    MappingResult,
    RowMapping,
    Sequence,
    TextClause,
    Result,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import Session

metadata_obj = MetaData()


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_sqlalchemy_version() -> str:
    return sqlalchemy.__version__


def display_hello_world(engine: Engine):
    """
    A simple Hello, World example using a SQL SELECT and a literal string
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    with engine.connect() as conn:
        result: CursorResult = conn.execute(text("select 'hello world'"))
        print(type(result))
        rows: Sequence[str] = result.all()
        print(type(rows))
        # print(rows)
        row: Row = rows[0]  # sqlalchemy.engine.row.Row
        # print(type(row))
        print(row)
        txt: str = row[0]
        # print(type(txt))
        print(txt)


def commit_as_you_go(engine: Engine):
    """
    Uses SQLAlchemy's built-in COMMIT capability to control when a batch of SQL DML actions are committed to the database.
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        result: CursorResult = conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()
        print(f"Rows inserted: {result.rowcount}")


def use_transaction_to_commit(engine: Engine):
    """Uses SQLAlchemy's built-in "BEGIN TRANSACTION" capability
    Assumes commit_as_you_go has been called previously
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")

    with engine.begin() as conn:
        result: CursorResult = conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )
        print(f"Rows inserted: {result.rowcount}")


def fetch_rows(engine: Engine):
    """
    Fetches rows from a table using various techniques.
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    with engine.connect() as conn:
        # access row contents using dot notation
        result: CursorResult = conn.execute(text("SELECT x, y FROM some_table"))
        row: Row
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

        # access row contents via column names:
        result: CursorResult = conn.execute(text("select x, y from some_table"))
        for x, y in result:
            print(f"x: {x}  y: {y}")

        # access row contents via positional index
        result = conn.execute(text("select x, y from some_table"))
        for row in result:
            x = row[0]
            y = row[1]
            print(f"x: {x}  y: {y}")


def fetch_rows_via_mappings(engine: Engine):
    """
    Fetches rows from a table using SQLAlchemy mappings that present each row as an instance of a RowMapping.
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    with engine.connect() as conn:
        result: CursorResult = conn.execute(text("select x, y from some_table"))
        mappings: MappingResult = result.mappings()
        dict_row: RowMapping
        for dict_row in mappings:
            x = dict_row["x"]
            y = dict_row["y"]
            print(f"x: {x}  y: {y}")


def fetch_rows_using_bound_parameter(engine: Engine):
    """
    Fetch rows from a table using a single bound parameter
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    with engine.connect() as conn:
        result: CursorResult = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2}
        )
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def fetch_rows_using_multiple_parameters(engine: Engine):
    """
    Fetch rows from a table using multiple parameters
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    with engine.connect() as conn:
        params: Sequence = [{"x": 11, "y": 12}, {"x": 13, "y": 14}]
        # NOTE: added DELETE, so we can run the program multiple times
        result: CursorResult = conn.execute(
            text("DELETE FROM some_table WHERE x = :x AND y = :y"), params
        )
        conn.commit()
        print(f"Rows deleted: {result.rowcount}")
        result: CursorResult = conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), params
        )
        conn.commit()
        print(f"Rows inserted: {result.rowcount}")


def orm_fetch_rows_using_parameter(engine: Engine):
    """
    Example of using SQLAlchemy Session to fetch multiple rows via a single parameter
    :type engine: Engine
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    # Notice we can use a DocString to make the SQL DML statement easier to read
    stmt: TextClause = text(
        """
        SELECT x, y 
           FROM some_table 
           WHERE y > :y 
           ORDER BY x, y;
        """
    )
    params: Sequence = {"y": 6}
    with Session(engine) as session:
        result: Result = session.execute(stmt, params)
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def orm_update_rows(engine: Engine):
    """
    Update multiple rows using ORM and parameters
    :type engine: object
    """
    print(f"\n{inspect.currentframe().f_code.co_name}")
    params: Sequence = [{"x": 9, "y": 11}, {"x": 13, "y": 15}]
    with Session(engine) as session:
        result: Result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"), params
        )
        session.commit()
        print(f"Rows affected: {result.rowcount}")


def display_table_columns(table: Table):
    print(f"table: {table.name}")
    for col in table.columns:
        primary_key: str = 'Primary Key' if col.primary_key else ''
        nullable: str = "NULL" if col.nullable else "NOT NULL"
        fk: set = col.foreign_keys
        foreign_key : str = ''
        if len(col.foreign_keys) > 0:
            fk = list(col.foreign_keys)[0]
            foreign_key = f'FK: {str(fk.column)}'
        print(f"\t{col.name:15}{str(col.type):15}{nullable:12}{primary_key:15}{foreign_key:15}")


def create_table_via_metadata(engine):
    print(f"\n{inspect.currentframe().f_code.co_name}")
    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )
    display_table_columns(user_table)


def create_table_with_foreign_key(engine):
    print(f"\n{inspect.currentframe().f_code.co_name}")
    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )
    display_table_columns(address_table)


if __name__ == "__main__":
    print(f"python version: {get_python_version()}")
    print(f"SQLAlchemy version: {get_sqlalchemy_version()}")

    engine: Engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    # print(type(engine))

    display_hello_world(engine)
    commit_as_you_go(engine)
    use_transaction_to_commit(engine)
    fetch_rows(engine)
    fetch_rows_via_mappings(engine)
    fetch_rows_using_bound_parameter(engine)
    fetch_rows_using_multiple_parameters(engine)
    orm_fetch_rows_using_parameter(engine)
    orm_update_rows(engine)
    create_table_via_metadata(engine)
    create_table_with_foreign_key(engine)
