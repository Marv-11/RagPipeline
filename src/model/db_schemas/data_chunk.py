from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    chunk_index: int = Field(..., gt=0, description="Index of the chunk within the file")
    chunk_text: str = Field(..., min_length=1, description="The actual text content of the chunk")
    metadata: dict = Field(default_factory=dict, description="Additional metadata for the chunk")
    project_id: str = Field(..., min_length=1, description="Identifier for the associated project")
    

    class Config:
        # Allow arbitrary types like ObjectId
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: lambda x: str(x)  # Convert ObjectId to string for JSON serialization
        }