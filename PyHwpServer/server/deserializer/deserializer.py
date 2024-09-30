import json
from pydantic import BaseModel
from config import load_config
from typing import Any

META_KEY = load_config().server.metadata.key


class HwpModel(BaseModel):
    metadata: dict[str, Any]
    text: dict[str, str]
    table: dict[str, list[list[str]]]


def _islistoflists(something)-> bool:
    if isinstance(something, list):
        if len(something) > 0:
            if isinstance(something[0], list):
                return True
    return False


def _islistofdict(something)-> bool:
    if isinstance(something, list):
        if len(something) > 0:
            if isinstance(something[0], dict):
                return True
    return False


def _getanddel(something):
    metadata = something[META_KEY]
    del something[META_KEY]
    return (metadata, something)


def _organizer(something: dict):
    result: dict = {}

    for key, value in something.items():
        if isinstance(value, dict):
            result.update(_organizer(value))
        elif _islistoflists(value) or isinstance(value, str):
            result[key] = value
        elif _islistofdict(value):
            for list_item in value:
                result.update(_organizer(list_item))
    return result


def to_hwp_model(something: dict):
    metadata:dict[str, any] = {}
    text:dict[str, str] = {}
    table: dict[str, list[list[str]]] = {}
    
    jsonified = json.loads(something)
    (metadata, jsonified) = _getanddel(jsonified)
    organized = _organizer(jsonified)

    for key, value in organized.items():
        if _islistoflists(value):
            table[key] = value
        elif isinstance(value, str):
            text[key] = value
    return HwpModel(text = text, table = table, metadata=metadata)
