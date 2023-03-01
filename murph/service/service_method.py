class ServiceMethod:
    def __init__(self, input_type=None, output_type=None, output_check=False):
        self.input_type = input_type
        self.output_type = output_type
        self.output_validation = output_check

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if self.output_validation:
                if not isinstance(result, self.output_type):
                    raise TypeError(f'{result} is not an instance of {self.output_type}')
            # Convert the class to a message
            return result.to_message()

        wrapper.__annotations__ = {
            'input_type': self.input_type,
            'output_type': self.output_type,
            'grpc_service_method': True
        }

        return wrapper
