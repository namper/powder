# -- Example

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action



class IOSerializationMixin: ...


class IOSerializer:
    def __init__(self, input_serializer, output_serialzier):
        pass



class InputSerialzier: ...

class OutputSerializer: ...


class SimpleViewSet(IOSerializationMixin, ViewSet):
    serialaizer_class = IOSerializer(
        input_serializer=InputSerialzier,
        output_serialzier=OutputSerializer
    )

    # Action performs reconstruction of view so i assume it will also inherit from 
    # IOSerializationMixin thus we don't need to overide @action decorator
    # We can re-use IOSerializer class 
    @action(
        serializer_class=IOSerializer(
            input_serializer=InputSerialzier,
            output_serialzier=OutputSerializer
        )
    )
    def x(self, request): return
