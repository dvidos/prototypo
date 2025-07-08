# service for {{ entity.name }} module


from sqlalchemy.orm import Session
from .entity import {{entity.name}}

class {{ entity.name }}Service:
    {% for action in service.actions %}
    def {{action.name | snake_case }}(self, db: Session):
    """
    Handle '{{ action }}' action for {{ entity.name }}.
    """
    # TODO: implement '{{ action }}' logic
    pass

    {% endfor %}
