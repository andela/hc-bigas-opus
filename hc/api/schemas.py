check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "timeout": {"type": "number", "minimum": 60, "maximum": 15552000},
        "grace": {"type": "number", "minimum": 60, "maximum": 15552000},
        "channels": {"type": "string"}
    }
}
