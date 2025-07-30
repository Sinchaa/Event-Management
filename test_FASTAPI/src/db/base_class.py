from typing import Any
from sqlalchemy.ext.declarative import declared_attr,declarative_base
from sqlalchemy.orm import as_declarative
from sqlalchemy import create_engine,MetaData

Base = declarative_base(metadata=MetaData(schema='public'))