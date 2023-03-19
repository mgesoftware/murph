from .message import export_message
from murph.service.handlers import RPCHandler


def export_service(service, stand_alone=False, complete_export=False) -> str:
    """Export service function"""

    proto_file = ''
    proto_file_header = ''
    if stand_alone or complete_export:
        proto_file_header += 'syntax = "{}";\n\n'.format(service.syntax)

        if service.package and service.package != "":
            proto_file_header += 'package {};\n\n'.format(service.package)

    proto_file += 'service {} {{\n'.format(type(service).__name__)

    function_objects = {
        name: getattr(service, name) for name in dir(service)
        if callable(getattr(service, name)) and not name.startswith("__")
    }

    service_messages = []
    for function_name, func in function_objects.items():
        if callable(func) and hasattr(func, '__annotations__'):
            annotations = func.__annotations__
            grpc_service_method = annotations.get('grpc_service_method')
            # Check if method is marked as a GRPC Method
            if not grpc_service_method:
                continue

            request_type = annotations.get('request_type')
            response_type = annotations.get('response_type')
            handler_type = annotations.get('handler_type')

            method_request = request_type.__name__
            method_response = response_type.__name__

            if handler_type == RPCHandler.CLIENT_STREAMING:
                method_request = "stream " + method_request
            elif handler_type == RPCHandler.SERVER_STREAMING:
                method_response = "stream " + method_response
            elif handler_type == RPCHandler.BIDIRECTIONAL_STREAMING:
                method_request = "stream " + method_request
                method_response = "stream " + method_response

            if complete_export:
                service_messages.append(request_type)
                service_messages.append(response_type)

            proto_file += '  rpc {}({}) returns ({});\n'.format(
                function_name,
                method_request,
                method_response
            )
    proto_file += '}'

    service_messages = list(set(service_messages))

    for message in service_messages:
        proto_file_header += export_message(message) + '\n'

    proto_file = proto_file_header + proto_file

    return proto_file
