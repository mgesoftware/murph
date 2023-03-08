from .base_meta import MessageMetaclass
from google.protobuf import descriptor
import inspect

# TODO: Non-repeatable indexes


class Message(metaclass=MessageMetaclass):
    """Base object with metaclass"""
    package = "murph.service_name"
    syntax = 'proto3'

    message_object = None  # Created in Initializer
    message_cls = None  # Created in Metaclass
    file_descriptor = None  # Created in Metaclass

    def __init__(self) -> None:
        self.message_object = self.message_cls()

    def __getattribute__(self, name):
        try:
            message_field_name = object.__getattribute__(self, "_fields_map")[name]
            return getattr(object.__getattribute__(self, "message_object"), message_field_name)
        except KeyError:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        try:
            message_field_name = self._fields_map[name]
            setattr(self.message_object, message_field_name, value)
        except KeyError:
            object.__setattr__(self, name, value)

    def validate(cls) -> None:
        """Validate the entire object"""
        super().validate(cls)

    def to_message(self) -> object:
        return self.message_object

    def to_file_descriptor_proto(cls) -> None:
        return cls._proto_descriptor.SerializeToString()

    @classmethod
    def get_proto_content(cls, stand_alone=False):
        default_implementation = descriptor._message
        field_map = {
            1: "double",
            2: "float",
            3: "int64",
            4: "uint64",
            5: "int32",
            6: "fixed64",
            7: "fixed32",
            8: "bool",
            9: "string",
            10: "group",
            11: "message",
            12: "bytes",
            13: "uint32",
            14: "enum",
            15: "sfixed32",
            16: "sfixed64",
            17: "sint32",
            18: "sint64"
        }

        fields = inspect.getmembers(cls.message_cls, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]

        # Write the .proto file header
        proto_file = ''
        if stand_alone:
            proto_file += 'syntax = "{}";\n\n'.format(cls.syntax)
            proto_file += 'package {};\n\n'.format(cls.package)

        proto_file += 'message {} {{\n'.format(cls.message_cls.__name__)

        # Write the fields of the message to the .proto file
        for field in fields:
            field_name = field[0]
            field_value = field[1]

            if isinstance(field_value, default_implementation.Descriptor):
                for descriptor_field in field_value.fields:
                    # TODO: Add support for message types and enum types
                    # if field.type == FieldDescriptorProto.TYPE_MESSAGE:
                    #     pass
                    # elif field.type == FieldDescriptorProto.TYPE_ENUM:
                    #     pass

                    field_name = descriptor_field.name
                    field_type = descriptor_field.type
                    field_number = descriptor_field.number
                    proto_file += '  {} {} = {};\n'.format(field_map[field_type], field_name, field_number)

        # Write the .proto file footer
        proto_file += '}\n'

        # Return the .proto file
        return proto_file
