from pydantic import BaseModel

class SystemPydanticModel(BaseModel):
    genpy: str
    filepath_checker_module: str

class FilePydanticModel(BaseModel):
    directory: str
    output_directory: str

class ImagePydanticModel(BaseModel):
    default_width: int
    default_height: int

class KafkaPydanticModel(BaseModel):
    host: str = None
    port: int = None
    str_type: str = None
    topic: str = None

class IntervalPydanticModel(BaseModel):
    loop: int

class MetadataPydanticModel(BaseModel):
    key: str
    template: str

class ServerPydanticModel(BaseModel):
    kafka: KafkaPydanticModel
    interval: IntervalPydanticModel
    metadata: MetadataPydanticModel

class ConfigPydanticModel(BaseModel):
    system: SystemPydanticModel
    file: FilePydanticModel
    image: ImagePydanticModel
    server: ServerPydanticModel