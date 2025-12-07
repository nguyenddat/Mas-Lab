import json
from typing import Any

from pydantic import BaseModel, create_model

def schema_to_pydantic(name: str, schema: dict) -> type[BaseModel]:
    fields = {}

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    for field, info in properties.items():
        field_type = Any
        default = ... if field in required else None
        fields[field] = (field_type, default)

    return create_model(f"{name}Args", **fields)

def normalize_mcp_response(resp):
    if resp and resp.content:
        text = resp.content[0].text
        return json.loads(text)
    return None