from pydantic import BaseModel
from typing import Any

class Return(BaseModel):
  type: str = "RETURN"
  value: str

class Await(BaseModel):
  type: str = "AWAIT"
  value: str

class Call(BaseModel):
  type: str = "CALL"
  route: str
  payload: dict[str, Any]

class Delegate(BaseModel):
  type: str = "DELEGATE"
  task: str

class GetStatus(BaseModel):
  type: str = "GET_STATUS"
  ticket_id: str