from .base_meta import MessageMeta
from google.protobuf.json_format import ParseDict
# TODO: Non-repeatable indexes


class Message(metaclass=MessageMeta):
    package = None
    syntax = 'proto3'

    def __init__(self, **kwargs):
        # self.__message_object__ = self.message_class()
        init_fields = None
        for key, value in kwargs.items():
            if key not in self.__fields__:
                raise AttributeError(f"{key} is not a valid field for {self.__class__.__name__}")
            init_fields = {self.__fields__[key].field_name: value}

        if init_fields:
            self.__message_object__ = ParseDict(init_fields, self.message_class())

    def __setattr__(self, name, value):
        if name != '__fields__' and name not in self.__fields__ and name != "__message_object__":
            raise AttributeError(f"{name} is not a valid field for {self.__class__.__name__}")
        super().__setattr__(name, value)

    @classmethod
    @property
    def message_class(cls) -> None:
        return cls.__message_class__

    @classmethod
    @property
    def file_descriptor(cls) -> None:
        return cls.__file_descriptor__

    @property
    def message_object(self) -> None:
        return self.__message_object__
