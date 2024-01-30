import json

def response_message(statuscode: int, message: str, payload=None):
    print(statuscode, message, payload)
    if not payload:
        payload = {}
    payload.update({'statusCode': statuscode, 'statusMessage': message})
    print(payload)
    return payload