from unittest.result import failfast

from core.parser import parse_blocks

def test_parser_comprehensive():
    text = """
    # A block with type and name
    entity Customer {
      Fullname                # type: None, name: Fullname
      string Email = "abc@x.com"  # type: string, name: Email, value: string
      Meta {
        CreatedBy
        CreatedAt
      }
    }

    # A block with only name
    Settings {
      Host = "localhost"
      Port = 8080
      Debug = true
      Logging {
        Level = "info"
        Enabled = true
      }
    }

    # A completely anonymous block
    {
      Note = "anonymous"
    }
    """

    blocks = parse_blocks(text)
    assert len(blocks) == 3

    # --- First block ---
    customer = blocks[0]
    assert customer.type == 'entity'
    assert customer.name == 'Customer'
    assert any(a.name == 'Fullname' and a.type is None for a in customer._assignments)
    assert any(a.name == 'Email' and a.type == 'string' and a.value == '"abc@x.com"' for a in customer._assignments)
    meta = next(c for c in customer.get_children() if c.name == 'Meta')
    assert any(f.name == 'CreatedBy' for f in meta._assignments)
    assert any(f.name == 'CreatedAt' for f in meta._assignments)

    # --- Second block ---
    settings = blocks[1]
    assert settings.type is None
    assert settings.name == 'Settings'
    assert any(a.name == 'Host' and a.value == '"localhost"' for a in settings._assignments)
    assert any(a.name == 'Port' and a.value == '8080' for a in settings._assignments)
    assert any(a.name == 'Debug' and a.value == 'true' for a in settings._assignments)
    logging = next(c for c in settings.get_children() if c.name == 'Logging')
    assert any(a.name == 'Level' and a.value == '"info"' for a in logging._assignments)
    assert any(a.name == 'Enabled' and a.value == 'true' for a in logging._assignments)

    # --- Third block (anonymous) ---
    anon = blocks[2]
    assert anon.type is None
    assert anon.name is None
    assert any(a.name == 'Note' and a.value == '"anonymous"' for a in anon._assignments)


def test_minimal_block():
    text = """
        {}
    """
    blocks = parse_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].type is None
    assert blocks[0].name is None

def test_same_line_block():
    text = """
        oneLiner {}
    """
    blocks = parse_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].type is None
    assert blocks[0].name == "oneLiner"


def test_minimal_error():
    text = """
    {
    }
    block1 {
    }
    entity block2 {
    }
    """
    blocks = parse_blocks(text)
    assert len(blocks) == 3
    assert blocks[0].type is None
    assert blocks[0].name is None
    assert blocks[1].type is None
    assert blocks[1].name == 'block1'
    assert blocks[2].type == 'entity'
    assert blocks[2].name == 'block2'
