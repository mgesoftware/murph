from google.protobuf import descriptor
import inspect


def export_message(message, stand_alone=False):
    """Export message function"""
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

    fields = inspect.getmembers(message.message_class, lambda a: not (inspect.isroutine(a)))
    fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]

    # Write the .proto file header
    proto_file = ''
    if stand_alone:
        proto_file += 'syntax = "{}";\n\n'.format(message.syntax)
        if message.package and message.package != "":
            proto_file += 'package {};\n\n'.format(message.package)

    proto_file += 'message {} {{\n'.format(message.message_class.__name__)

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
                if descriptor_field.type == 11:
                    # DEFINESTE TIPUL DE DATA MESSAGE
                    # REDENUMESTE VARIABILA field_type_name
                    # descriptor_field.label REDENUMIRE
                    # field_type_name = descriptor_field.type_name
                    print(descriptor_field)
                else:
                    field_type_name = field_map[field_type]

                if descriptor_field.label == 3:
                    # Repeated field
                    proto_file += '  repeated {} {} = {};\n'.format(field_type_name, field_name, field_number)
                else:
                    proto_file += '  {} {} = {};\n'.format(field_type_name, field_name, field_number)

    # Write the .proto file footer
    proto_file += '}\n'

    # Return the .proto file
    return proto_file
