from google.protobuf.descriptor_pb2 import FieldDescriptorProto, DescriptorProto
from .fields import Field
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf.descriptor_pb2 import FileDescriptorProto


class MessageMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        proto_fields = []

        # FOR FIELD GENERATION
        skipped_fields = []
        used_indexes = []

        for key, value in attrs.items():
            if isinstance(value, Field):
                value.name = key
                type_name = None
                # if the field_name is not specified, use the variable name
                if not value.field_name:
                    value.field_name = key
                    attrs[key].field_name = key

                fields[key] = value

                if value.index is None:
                    skipped_fields.append((key, value))
                else:
                    used_indexes.append(value.index)
                    # CREATE FIELD FOR
                    if value.field_type == 11:
                        type_name = f".{value.message_class.__name__}"
                        if value.message_class.package and value.message_class.package != "":
                            type_name = f".{value.message_class.package}{type_name}"
                    proto_fields.append(
                        FieldDescriptorProto(
                            name=value.field_name if value.field_name else key,
                            number=value.index,
                            label=value.label,
                            type=value.field_type,
                            type_name=type_name
                        )
                    )
                    # print(proto_fields[len(proto_fields) - 1])
        # Generate field indexes
        indexes = len(used_indexes) + len(skipped_fields)
        # Sort the indexes so they will always get the same value
        sorted_skipped_fields = sorted(skipped_fields, key=lambda x: x[0])
        available_indexes = [i for i in range(1, indexes + 1) if i not in used_indexes]

        # Create unassigned fields
        for field in sorted_skipped_fields:
            key = field[0]
            value = field[1]
            index = available_indexes.pop(0)
            attrs[key].index = index
            type_name = None

            if value.field_type == 11:
                type_name = f".{value.message_class.__name__}"
                if value.message_class.package and value.message_class.package != "":
                    type_name = f".{value.message_class.package}{type_name}"

            proto_fields.append(
                FieldDescriptorProto(
                    name=value.field_name if value.field_name else key,
                    number=index,
                    label=value.label,
                    type=value.field_type,
                    type_name=type_name
                )
            )

        proto_descriptor = DescriptorProto(
            name=name,
            field=proto_fields
        )

        attrs['__fields__'] = fields
        attrs['__fields_descriptor_proto__'] = proto_fields
        attrs['__descriptor_proto__'] = proto_descriptor

        # Get message base class
        if not bases:
            # if this is not a child class, return
            return super().__new__(cls, name, bases, attrs)

        message_base = bases[0]

        file_descriptor_proto = FileDescriptorProto(
            name=f'{proto_descriptor.name.lower()}.proto',
            package=message_base.package if message_base.package != "" else None,
            syntax=message_base.syntax,
            message_type=[proto_descriptor]
        )

        scope = {}
        file_descriptor = _descriptor_pool.Default().AddSerializedFile(file_descriptor_proto.SerializeToString())

        _builder.BuildMessageAndEnumDescriptors(file_descriptor, scope)
        _builder.BuildTopDescriptorsAndMessages(
            file_descriptor, f'protobufs.{proto_descriptor.name.lower()}_pb2', scope
        )

        _builder.BuildMessageAndEnumDescriptors(file_descriptor, globals())
        _builder.BuildTopDescriptorsAndMessages(
            file_descriptor, f'protobufs.{proto_descriptor.name.lower()}_pb2', globals()
        )

        # Get the Message class
        attrs['__message_class__'] = scope[name]
        attrs['__file_descriptor__'] = file_descriptor
        attrs['__file_descriptor_proto__'] = file_descriptor_proto

        return super().__new__(cls, name, bases, attrs)
