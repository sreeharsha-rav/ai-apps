from pydantic import BaseModel, Field
from typing import List


class ContextItem(BaseModel):
    type: str = Field(
        description="Type of the context item"
    )
    content: str = Field(
        description="Content of the context item"
    )

class Context(BaseModel):
    items: List[ContextItem] = Field(
        default=[],
        description="List of context items"
    )
