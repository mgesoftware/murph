import grpc
from .base_meta import ServiceMetaclass


class Service(metaclass=ServiceMetaclass):
    package = None
    syntax = "proto3"

    def default_handler(self, handler_call_details, request, context):
        """The default handler, when no other handlers are found"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not found!')

        raise NotImplementedError('Method not found!')

    def service(self, handler_call_details):
        """The handler server for the gRPC Service"""
        try:
            handler = self._handlers[handler_call_details.method]
        except KeyError:
            handler = grpc.unary_unary_rpc_method_handler(
                lambda request, context: self.default_handler(handler_call_details, request, context),
            )

        return handler

    @classmethod
    def export_to_proto_file(cls, stand_alone=False, complete_export=False):

        proto_file = ''
        proto_file_header = ''
        if stand_alone or complete_export:
            proto_file_header += 'syntax = "{}";\n\n'.format(cls.syntax)
            proto_file_header += 'package {};\n\n'.format(cls.package)

        proto_file += 'service {} {{\n'.format(cls.__name__)

        function_objects = {
            name: getattr(cls, name) for name in dir(cls) if callable(getattr(cls, name)) and not name.startswith("__")
        }

        service_messages = []
        for function_name, func in function_objects.items():
            if callable(func) and hasattr(func, '__annotations__'):
                annotations = func.__annotations__
                grpc_service_method = annotations.get('grpc_service_method')
                # Check if method is marked as a GRPC Method
                if not grpc_service_method:
                    continue
                input_type = annotations.get('input_type')
                output_type = annotations.get('output_type')

                if complete_export:
                    service_messages.append(input_type)
                    service_messages.append(output_type)

                proto_file += '  rpc {}({}) returns ({});\n'.format(
                    function_name,
                    input_type.__name__,
                    output_type.__name__
                )
        proto_file += '}'

        service_messages = list(set(service_messages))

        for message in service_messages:
            proto_file_header += message.export_to_proto_file() + '\n'

        proto_file = proto_file_header + proto_file
        return proto_file
