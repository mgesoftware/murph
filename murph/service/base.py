from .base_meta import ServiceMetaclass


class Service(metaclass=ServiceMetaclass):
    package = None
    syntax = "proto3"

    def get_handlers(self):
        return self._handlers
