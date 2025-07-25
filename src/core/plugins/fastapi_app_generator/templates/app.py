from fastapi import FastAPI
from databases import Database
from pydantic import BaseModel
from controllers import {% for controller in controllers %}{{ controller.name|lower }}{% if not loop.last %}, {% endif %}{% endfor %}


app = FastAPI()

DATABASE_URL = "{{ db_url }}"
database = Database(DATABASE_URL)

{% for controller in controllers %}
app.include_router({{controller.name | lower}}.router, prefix="/api/{{ controller.name|lower }}", tags=["{{ controller.name|lower }}"])
{% endfor %}



@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class Item(BaseModel):
    id: int
    name: str

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     query = "SELECT id, name FROM items WHERE id = :item_id"
#     result = await database.fetch_one(query=query, values={"item_id": item_id})
#     if result:
#         return {"id": result['id'], "name": result['name']}
#     return {"error": "Item not found"}

