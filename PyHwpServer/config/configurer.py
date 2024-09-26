import yaml
from pydantic import create_model
from util import capitalize_first_letter
from .config import ConfigPydanticModel

YAMLFILE = './py_hwp.yaml'

def _load_yaml():
    with open(YAMLFILE) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config


def _generate_pydantic_model(data: dict, modelname):
    fields = {}
    for key, value in data.items():
        if isinstance(value, dict):
            fields[key] = (_generate_pydantic_model(value, key), ...)
        else:
            fields[key] = (type(value), ...)
    
    return create_model(capitalize_first_letter(modelname)+"PydanticModel", **fields)


def load_config() -> ConfigPydanticModel:
    config = _load_yaml()
    Configurer = _generate_pydantic_model(config, "Dynamic")
    config_model: ConfigPydanticModel = Configurer(**config).config

    return config_model
