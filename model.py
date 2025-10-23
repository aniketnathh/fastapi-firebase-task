from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SignUpSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "samplepass123",
                "full_name": "John Doe"
            }
        }


class LogInSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "samplepass123"
            }
        }


class UpdateUserSchema(BaseModel):
    full_name: str

    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe Updated"
            }
        }


class TaskCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, Eggs, Bread"
            }
        }


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskResponseSchema(BaseModel):
    task_id: str
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
