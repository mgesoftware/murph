import grpc
import types


class ServiceMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # Get the list of all functions defined by user
        function_objects = {name: value for name, value in attrs.items() if callable(value) and not name.startswith('__')}
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

                input_type = annotations.get('input_type')
                output_type = annotations.get('output_type')

                if input_type:
                    request_deserializer = input_type.message_class.FromString

                if output_type:
                    response_serializer = output_type.message_class.SerializeToString
            else:
                # If it's not callable or the method wasn't decorated with ServiceMethod it means 
                # that we don't have a grpc method so we skip
                continue

            # Add the handler for grpc method to _handlers variable
            function_handler = {
                f"{function_name}":
                    grpc.unary_unary_rpc_method_handler(
                        types.MethodType(func, object()),  # Make a bound method
                        request_deserializer=request_deserializer,
                        response_serializer=response_serializer,
                    )
            }
            attrs['_handlers'].update(function_handler)
        # Create the class with the modified attributes
        return super().__new__(cls, name, bases, attrs)
