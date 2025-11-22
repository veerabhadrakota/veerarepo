from pydantic import Field, BaseModel

class JsonSerializableModel(BaseModel):
    """A base model that provides a JSON string representation."""

    def __str__(self) -> str:
        return self.model_dump_json(indent=2)