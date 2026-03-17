# Logic Pro Toolkit Documentation

## Quick Start

```python
from logic_toolkit import LogicProClient

client = LogicProClient()
if client.is_installed():
    client.connect()
    print(f"Version: {client.get_version()}")
```

## API Reference

See individual module documentation.
