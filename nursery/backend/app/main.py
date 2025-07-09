from fastapi import FastAPI
from app.controllers import customer_controller, order_controller

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "hello world"}

app.include_router(customer_controller.router)
app.include_router(order_controller.router)
