from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.customer import customer_controller
from app.modules.order import order_controller
from app.modules.order_status import order_status_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React dev server local
        "http://frontend:3000",    # Docker service hostname
        # add any other URLs your frontend might use
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"message": "hello world"}

app.include_router(customer_controller.router, prefix="/api/customers")
app.include_router(order_controller.router, prefix="/api/orders")
app.include_router(order_status_controller.router, prefix="/api/order_statuses")
