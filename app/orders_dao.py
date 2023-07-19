import os

from sqlmodel import SQLModel, create_engine, Session

from models import Order


PGSQL_HOST = os.getenv("PGSQL_HOST", "localhost")
PGSQL_PORT = os.getenv("PGSQL_PORT", 5432)
PGSQL_PASSWORD = os.getenv("PGSQL_PASSWORD", "postgres")
PGSQL_USERNAME = os.getenv("PGSQL_USERNBAME", "postgres")


class OrdersDao:
    def __init__(self):
        self._engine = create_engine(f"postgresql://{PGSQL_USERNAME}:{PGSQL_PASSWORD}@{PGSQL_HOST}:{PGSQL_PORT}")

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self._engine)

    def create_order(self, order: Order):
        with Session(self._engine) as session:
            session.add(order)
            session.commit()
            session.refresh(order)
            return order

    def update_order_status(self, order_id, status):
        with Session(self._engine) as session:
            order = session.get(Order, order_id)
            setattr(order, "status", status)
            session.add(order)
            session.commit()
            session.refresh(order)
            return order


dao = OrdersDao()
