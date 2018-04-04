check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "timeout": {"type": "number", "minimum": 60, "maximum": 15552000},
        "grace": {"type": "number", "minimum": 60, "maximum": 15552000},
        "timeout": {"type": "number", "minimum": 60, "maximum": 604800},
        "grace": {"type": "number", "minimum": 60, "maximum": 604800},
        "nag":{"type": "number", "minimum": 60, "maximum":604800},
        "channels": {"type": "string"}
    }
}
