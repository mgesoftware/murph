from google.protobuf.descriptor_pb2 import FieldDescriptorProto, DescriptorProto
from .fields import Field
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.descriptor_pb2 import FileDescriptorProto


class MessageMetaclass(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)

        # Start validation methods
        validation_methods = {}

        for field_name, field_instance in namespace.items():
            if isinstance(field_instance, Field):
                validation_methods[f"{field_name}_validate"] = cls.create_validate_method(field_name)

        namespace.update(validation_methods)
        setattr(cls, "validate", cls.create_validate_all_method(cls))

    def __new__(mcls, name, bases, attrs):
        proto_fields = []
        fields_map = {}

        for field in attrs:
            field_obj = attrs[field]
            if isinstance(field_obj, Field):
                proto_fields.append(
                    FieldDescriptorProto(
                        name=field_obj.name if field_obj.name else field,
                        number=field_obj.index,
                        label=field_obj.label,
                        type=field_obj.field_type
                    )
                )
                fields_map[field] = field_obj.name

        proto_descriptor = DescriptorProto(
            name=name,
            field=proto_fields
        )

        attrs['_fields_map'] = fields_map
        attrs['_proto_fields'] = proto_fields
        attrs['_proto_descriptor'] = proto_descriptor

        # Get message base class
        if not bases:
            # if it's not inherited then return the class
            return super().__new__(mcls, name, bases, attrs)

        message_base = bases[0]

        file_desc_proto = FileDescriptorProto(
            name=f'{proto_descriptor.name.lower()}.proto',
            package=message_base.package,
            syntax=message_base.syntax,
            message_type=[proto_descriptor]
        )

        scope = {}
        _sym_db = _symbol_database.Default()
        file_descriptor = _descriptor_pool.Default().AddSerializedFile(file_desc_proto.SerializeToString())

        _builder.BuildMessageAndEnumDescriptors(file_descriptor, scope)
        _builder.BuildTopDescriptorsAndMessages(file_descriptor, f'protobufs.{proto_descriptor.name.lower()}_pb2', scope)

        _builder.BuildMessageAndEnumDescriptors(file_descriptor, globals())
        _builder.BuildTopDescriptorsAndMessages(file_descriptor, f'protobufs.{proto_descriptor.name.lower()}_pb2', globals())

        # Get the message class
        attrs['message_cls'] = scope[name]
        attrs['file_descriptor'] = file_descriptor

        return super().__new__(mcls, name, bases, attrs)

    @staticmethod
    def create_validate_method(field_name):
        def validate_method(self):
            """Default validate created by metaclass"""
        return validate_method

    @staticmethod
    def create_validate_all_method(cls):
        def validate(self):
            validate_functions = []

            for attr in self._fields_map:
                validate_functions.append(f"{attr}_validate")

            for attr_name in dir(self):
                if attr_name in validate_functions:
                    validate_method = getattr(self, attr_name)
                    validate_method()
        return validate
