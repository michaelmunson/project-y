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

class LoadTicket(BaseModel):
  type: str = "LOAD_TICKET"
  ticket_id: str

class UnloadTicket(BaseModel):
  type: str = "UNLOAD_TICKET"
  ticket_id: str