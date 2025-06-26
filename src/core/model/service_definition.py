from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ServiceDefinition:
    """ Represents one service that runs from docker-compose or k8s

    It can serve various purposes:
    - front end
    - back end
    - database
    - message broker
    - caching server
    - documentation presenter
    - other metrics, logging, alerting, authorizing, etc stack.
    """
    name: str
    build_path: Optional[str] = None
    dockerfile: Optional[str] = None
    image: Optional[str] = None
    environment: Dict[str, str] = field(default_factory=dict)
    ports: List[str] = field(default_factory=list)
    volumes: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    command: Optional[str] = None
