
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
from fastapi.background import BackgroundTasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
        allow_methods = ["*"],
        allow_headers = ["*"]
)

redis = get_redis_connection(
    host = "redis-17797.c251.east-us-mz.azure.cloud.redislabs.com",
    port = 17797,
    password = "sSCNMhZoiAQ4YTieysTMD0zXDkjQGH5o",
    decode_responses = True
)

class Order(HashModel):
    product_id : str
    price: float
    fee: float
    total: float
    quantity: int
    status : str # pending, completed, refunded

    class Meta:
        database = redis

@app.get("/orders/{pk}")
async def get_order(pk: str):
    return Order.get(pk)

@app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks): #id and quantity
    body  = await request.json()
    req = requests.get("http://localhost:8000/products/%s" %body['id'])
    product = req.json()

    order  = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2* product['price'],
        total = 1.2* product['price'],
        quantity = body['quantity'],
        status = "pending"
    )
    order.save()
    background_tasks.add_task(order_completed, order)

    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
