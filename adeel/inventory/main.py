
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


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

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get("/products")
def all_products():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.post("/products")
def create_product(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get_product(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete_product(pk: str):
    Product.delete(pk)
    return {"message": "Product deleted successfully!"}
