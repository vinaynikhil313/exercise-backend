import logging
import time

from fastapi import BackgroundTasks

import stock_exchange
from models import CreateOrderModel, CreateOrderResponseModel, Order, OrderStatus
from orders_dao import dao
from stock_exchange import OrderPlacementError

PLACE_ORDER_MAX_RETRIES = 5

logger = logging.getLogger(__name__)


def create_and_place_order(order_request: CreateOrderModel, background_tasks: BackgroundTasks) \
        -> CreateOrderResponseModel:
    order = order_request.to_order_entity()
    order = dao.create_order(order)
    try:
        stock_exchange.place_order(order)
        order = dao.update_order_status(order.id, OrderStatus.SUCCESS)
    except OrderPlacementError:
        logger.warning(f"Error while placing order with id {order.id}. Order placement will be retried")
        background_tasks.add_task(retry_order_placement, order)
    return order


def retry_order_placement(order: Order):
    for i in range(PLACE_ORDER_MAX_RETRIES):
        try:
            time.sleep(2)
            stock_exchange.place_order(order)
            order = dao.update_order_status(order.id, OrderStatus.SUCCESS)
            return
        except OrderPlacementError:
            logger.warning(f"Order placement for id {order.id} failed on retry attempt {i+1}")
    logger.error(f"Order placement for id {order.id} failed even after {PLACE_ORDER_MAX_RETRIES} attempts. "
                 f"Status will be updated to failure.")
    dao.update_order_status(order.id, OrderStatus.FAILURE)
