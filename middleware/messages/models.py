from pydantic import BaseModel
from typing import Any, Dict, List

class ReturnMessages(BaseModel):
  statusCode: int
  statusMessage: str
  errorMessage: str | None=None
  messages: list | None=None

class SearchMessages(BaseModel):
  statusCode: int
  statusMessage: str
  errorMessage: str | None=None
  messages: list | None=None

class CreateMessageResponse(BaseModel):
  statusCode: int
  statusMessage: str
  errorMessage: str | None=None
  message_id: str | None=None