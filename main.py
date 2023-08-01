"""
https://docs.sqlalchemy.org/en/20/tutorial/engine.html
"""

import sys

import sqlalchemy
from sqlalchemy import create_engine


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_sqlalchemy_version() -> str:
    return sqlalchemy.__version__


if __name__ == "__main__":
    print(f"python version: {get_python_version()}")
    print(f'SQLAlchemy version: {get_sqlalchemy_version()}')
