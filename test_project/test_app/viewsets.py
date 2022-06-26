from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from test_app.models import Simple
from powder.drf.dispatch import dispatch_serializer


class SimpleSeriazlier(ModelSerializer):
    class Meta:
        model = Simple
        fields = ('id', 'name')


class ListSerializer(ModelSerializer):
    class Meta:
        model = Simple
        fields = '__all__'


class SimpleViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Simple.objects.all()

    serializer_dispatcher = dispatch_serializer(
        fallback_serializer=SimpleSeriazlier,
        list_serializer=ListSerializer
    )
    # @TODO: FIX typing
    serializer_class = serializer_dispatcher

