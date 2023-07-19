import logging

from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from models import CreateOrderResponseModel, CreateOrderModel
from orders_dao import dao
from orders_service import create_and_place_order

logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("Creating tables")
    dao.create_db_and_tables()


@app.post(
    "/orders",
    status_code=201,
    response_model=CreateOrderResponseModel,
    response_model_by_alias=True,
)
async def create_order(create_order_request: CreateOrderModel, background_tasks: BackgroundTasks):
    return create_and_place_order(create_order_request, background_tasks)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error while placing the order"}
    )
