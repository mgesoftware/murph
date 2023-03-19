"""Definition of all available fields"""
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
# from .base import Message


class Field:
    field_type = None

    def __init__(self, index: int = None, field_name: str = None, repeated: bool = False):
        self.field_name = field_name
        self.index = index
        self.label = 1
        self.repeated = repeated

        if self.repeated:
            self.label = 3  # REPEATED FIELD

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.__message_object__, self.field_name)

    def __set__(self, instance, value):
        # if self.repeated:
        #     instance.__message_object__.CopyFrom(value)
        # else:
        setattr(instance.__message_object__, self.field_name, value)


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


class MessageField(Field):
    """ Message Field definition"""
    field_type = FieldDescriptorProto.TYPE_MESSAGE

    def __init__(self, message, index: int = None, field_name: str = None, repeated: bool = False):
        self.message_class = message
        super().__init__(index=index, field_name=field_name, repeated=repeated)
