import databases
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, BigInteger

DATABASE_URL = "postgresql://myuser:mypassword@db:5432/mydatabase"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

prices = Table(
    "prices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ticker", String(10), nullable=False),
    Column("price", Numeric(18, 8), nullable=False),
    Column("timestamp", BigInteger, nullable=False)
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
