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

class ConfigPydanticModel(BaseModel):
    system: SystemPydanticModel
    file: FilePydanticModel
    image: ImagePydanticModel