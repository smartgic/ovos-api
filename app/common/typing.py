"""Add some custom Pydantic typing
"""
from typing import Any, Dict, AnyStr, List, Union

# {"key": 1} or {"key": "value"} or {"key": {}}, etc...
JSONObject = Dict[AnyStr, Any]

# ["string"], [["string"]], [{"key": "value"}], etc...
JSONArray = List[Any]

# Merge or both types
JSONStructure = Union[JSONArray, JSONObject]
