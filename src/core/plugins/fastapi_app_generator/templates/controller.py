from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# {{ controller.name }}

router = APIRouter()

# --- data models used in http endpoints ---

{% for data_model in controller.models %}
{% if data_model.attributes %}
class {{ data_model.name }}(BaseModel):
    {% for attr, attr_type in data_model.attributes.items() %}
    {{ attr }}: {{ attr_type }}
    {% endfor %}
{% else %}
class {{ data_model.name }}(BaseModel):
    pass
{% endif %}

{% endfor %}

# --- actual http endpoints ---

{% for endpoint in controller.endpoints %}
@router.{{ endpoint.method | lower }}("{{ endpoint.path }}", name="{{ endpoint.name }}", summary="{{ endpoint.summary }}")
async def {{ endpoint.handler_name }}(
    {%- if endpoint.identifier_name and endpoint.request_model -%}
        {{ endpoint.identifier_name }}: int, request: {{ endpoint.request_model }}
    {%- elif endpoint.identifier_name and not endpoint.request_model -%}
        {{ endpoint.identifier_name }}: int
    {%- elif not endpoint.identifier_name and endpoint.request_model -%}
        request: {{ endpoint.request_model }}
    {%- endif -%}
) -> {{ endpoint.response_model if endpoint.response_model else 'dict' }}:
    # TODO: Implement the logic for {{ endpoint.name }}
    return {"message": "Endpoint {{ endpoint.name }} is not implemented yet"}

{% endfor %}
