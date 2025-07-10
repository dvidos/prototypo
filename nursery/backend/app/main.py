from fastapi import FastAPI
from app.modules.customer import customer_controller
from app.modules.order import order_controller

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "hello world"}

app.include_router(customer_controller.router)
app.include_router(order_controller.router)
