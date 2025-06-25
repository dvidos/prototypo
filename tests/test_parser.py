from core.parser import parse_entities

def test_simple_entity_parsing():
    text = """
    entity Customer {
      fields {
        Name
        Email
      }
    }
    """
    entities = parse_entities(text)
    assert len(entities) == 1
    assert entities[0]['name'] == 'Customer'
    assert entities[0]['fields'] == ['Name', 'Email']
