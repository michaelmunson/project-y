from pydantic import BaseModel
from typing import Any

"""
End of Task - Return a value
"""
class Return(BaseModel):
  type: str = "RETURN"
  value: str

"""
Await Task - Await a value from a ticket
"""
class AwaitTicket(BaseModel):
  type: str = "AWAIT"
  value: str

"""
Call Task - Call a function
"""
class Call(BaseModel):
  type: str = "CALL"
  route: str
  payload: dict[str, Any]

"""
Delegate Task - Delegate a task to a ticket
"""
class Delegate(BaseModel):
  type: str = "DELEGATE"
  task: str

