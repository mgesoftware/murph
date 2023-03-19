from .handlers import create_rpc_method_handler
import types


class ServiceMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # Get the list of all functions defined by user
        function_objects = {
            name: value for name, value in attrs.items()
            if callable(value) and not name.startswith('__')
        }
        attrs['_handlers'] = {}

        # Create handlers for each service method
        for function_name, func in function_objects.items():
            request_deserializer = None
            response_serializer = None

            if callable(func) and hasattr(func, '__annotations__'):
                annotations = func.__annotations__
                grpc_service_method = annotations.get('grpc_service_method')
                # Check if method is marked as a GRPC Method
                if not grpc_service_method:
                    continue

                request_type = annotations.get('request_type')
                response_type = annotations.get('response_type')

                if request_type:
                    request_deserializer = request_type.message_class.FromString

                if response_type:
                    response_serializer = response_type.message_class.SerializeToString
            else:
                # If it's not callable or the method wasn't decorated with grpc_method it means
                # that we don't have a grpc method so we skip
                continue

            # Add the handler for grpc method to _handlers variable
            handler_type = annotations.get('handler_type')
            handler = create_rpc_method_handler(handler_type)
            function_handler = {
                f"{function_name}":
                    handler(
                        types.MethodType(func, object()),  # Make a bound method
                        request_deserializer=request_deserializer,
                        response_serializer=response_serializer,
                    )
            }
            attrs['_handlers'].update(function_handler)
        # Create the class with the modified attributes
        return super().__new__(cls, name, bases, attrs)
