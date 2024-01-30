from typing import Annotated

from fastapi import APIRouter, Header, Depends, Query
from fastapi.encoders import jsonable_encoder

from utils.response import response_message
from .models import SearchMessages, ReturnMessages, CreateMessageResponse
from . import messages_manager

messages_router=APIRouter()


def create_call_param_check(
    account_id: str = Query(None),
    sender_number: str = Query(None),
    receiver_number: str = Query(None)
):
    if account_id is None or sender_number is None or receiver_number is None:
        return None
    return account_id, sender_number, receiver_number

@messages_router.post("/create", tags=["create messages"], response_model=CreateMessageResponse)
async def create_message(params: tuple = Depends(create_call_param_check)):
  if params is None:
    return response_message(200,"Success", dict(errorMessage="message_id or sender_no or receiver_no is missing"))
  account_id, sender_number, receiver_number = params
  return response_message(*messages_manager.create_message(account_id, sender_number, receiver_number))

@messages_router.get("/get/messages/{account_id}", tags=["get messages"], response_model=ReturnMessages)
async def get_messages(account_id):
  return response_message(*messages_manager.get_messages(account_id))

def at_least_one_parameter(
    message_id: str = Query(None),
    sender_no: str = Query(None),
    receiver_no: str = Query(None)
):
    if message_id is None and sender_no is None and receiver_no is None:
      return None
    return message_id, sender_no, receiver_no

@messages_router.get("/search", tags=["search messages"], response_model=SearchMessages)
async def search_messages(params: tuple = Depends(at_least_one_parameter)):
    if params is None:
      return response_message(200,"Success", dict(errorMessage="At least one of message_id or sender_no or receiver_no must be provided"))
    message_id, sender_no, receiver_no = params
    return response_message(*messages_manager.search_message(message_id, sender_no, receiver_no))