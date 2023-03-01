"""Definition of all available fields"""
from google.protobuf.descriptor_pb2 import FieldDescriptorProto


class Field:
    """ Default field implementation """
    field_type = None

    def __init__(
        self, index: int, name: str = None, repeated: bool = False, optional: bool = False, default=None
    ) -> None:
        self.name = name
        self.index = index
        self.label = 1
        self.repeated = repeated
        self.optional = optional
        self.value = default


class DoubleField(Field):
    """ Int32 field definition """
    field_type = FieldDescriptorProto.TYPE_DOUBLE


class FloatField(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_FLOAT


class Int64Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_INT64


class UInt64Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_UINT64


class Int32Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_INT32


class Fixed64Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_FIXED64


class Fixed32Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_FIXED32


class BoolField(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_BOOL


class StringField(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_STRING


class BytesField(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_BYTES


class UInt32Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_UINT32


class EnumField(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_ENUM


class SFixed32Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_SFIXED32


class SFixed64Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_SFIXED64


class SInt32Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_SINT32


class SInt64Field(Field):
    """ String field definition """
    field_type = FieldDescriptorProto.TYPE_SINT64
