from pydantic import BaseModel, Field


# ----------------------------------
# Auth Schemas
# ----------------------------------
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "myuser",
                "password": "mypassword"
            }
        }
    }

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "myuser",
                "password": "mypassword"
            }
        }
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "mytoken",
                "token_type": "bearer"
            }
        }
    }

# ----------------------------------
# Todo Schemas
# ----------------------------------
class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6, description="Priority between 1-5")
    completed: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My Todo",
                "description": "My Todo Description",
                "priority": 1,
                "completed": False
            }
        }
    }

class TodoResponse(BaseModel):
    id: str
    title: str
    description: str
    priority: int
    completed: bool
    owner: str

    model_config = {
        "from_attributes": True
    }