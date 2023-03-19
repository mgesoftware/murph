from murph.message import Message
from .handlers import RPCHandler


def grpc_method(request_type: Message, response_type: Message, handler_type: RPCHandler):
    def decorator(func):
        func.__annotations__ = {
            'request_type': request_type,
            'response_type': response_type,
            'handler_type': handler_type,
            'grpc_service_method': True
         }
        return func

    return decorator
