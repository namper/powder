import pytest

from typing import Type, Optional, Callable

from django.db import models
from django.test import TestCase

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.test import APIRequestFactory

from powder.drf.dispatch import dispatch_serializer, DispatcherProxy


factory = APIRequestFactory()

class SimpleModel(models.Model):
    name = models.CharField(max_length=10)

class TestDispatcher(TestCase):

    def test_dispatches_fallback(self):
        class FallbackSerialzier(serializers.ModelSerializer):
            class Meta:
                model = SimpleModel
                fields = '__all__'

        class SimpleViewSet(ModelViewSet):
            queryset = SimpleModel.objects.all()
            serializer_class: DispatcherProxy = dispatch_serializer(
                fallback_serializer=FallbackSerialzier
            )

        view = SimpleViewSet.as_view(
            actions={
                'get': 'list'
            }
        )
        request = factory.get('/', '', content_type='application/json')
        response = view(
            request=request
        ) # type: ignore

        print(response)
