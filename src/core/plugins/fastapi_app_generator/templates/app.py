from fastapi import FastAPI
from databases import Database
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "{{ db_url }}"
database = Database(DATABASE_URL)

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

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = "SELECT id, name FROM items WHERE id = :item_id"
    result = await database.fetch_one(query=query, values={"item_id": item_id})
    if result:
        return {"id": result['id'], "name": result['name']}
    return {"error": "Item not found"}

{# Endpoints definitions #}
{% for endpoint in endpoints %}
@app.{{ endpoint.method }}("{{ endpoint.path }}", name="{{ endpoint.name }}", summary="{{ endpoint.summary }}")
async def {{ endpoint.name }}(
    {% if endpoint.request_model %}request: {{ endpoint.request_model }},{% endif %}
) -> {% if endpoint.response_model %}{{ endpoint.response_model }}{% else %}dict{% endif %}:
    # TODO: Implement the logic for {{ endpoint.name }}
    return {"message": "Endpoint {{ endpoint.name }} is not implemented yet"}
{% endfor %}
