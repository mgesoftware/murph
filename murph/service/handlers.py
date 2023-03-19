import enum
import grpc


class RPCHandler(enum.Enum):
    UNARY = 1
    SERVER_STREAMING = 2
    CLIENT_STREAMING = 3
    BIDIRECTIONAL_STREAMING = 4


def create_rpc_method_handler(handler_type: RPCHandler):
    handlers = {
        RPCHandler.UNARY: grpc.unary_unary_rpc_method_handler,
        RPCHandler.SERVER_STREAMING: grpc.unary_stream_rpc_method_handler,
        RPCHandler.CLIENT_STREAMING: grpc.stream_unary_rpc_method_handler,
        RPCHandler.BIDIRECTIONAL_STREAMING: grpc.stream_stream_rpc_method_handler
    }

    return handlers[handler_type]
