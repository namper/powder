from typing import  TypeVar,  Callable
from rest_framework.serializers import BaseSerializer
from functools import partial
from enum import Enum


T = TypeVar("T", bound=BaseSerializer)


class Action(str, Enum):
    LIST  =  "list"
    RETRIEVE = "retrieve"
    CREATE = "create"
    UNKNOWN = "unknown"


def _extract_request_action(context: dict | None) -> Action:
    if isinstance(context, dict) and (request := context.get('request')):
        return Action(
            getattr(request, "action", "unknown")
        )
    return Action.UNKNOWN



def _construct_serializer(get_serializer_class: Callable[[Action], type[T]], *args, **kwargs) -> T:
    serialzier_class = get_serializer_class(
        _extract_request_action(kwargs.get('context'))
    )
    return serialzier_class(*args, **kwargs)



_T = TypeVar("_T")

def _fall_back(instance: _T | None, fallback: _T) -> _T:
    return instance or fallback


def dispatch_serializer(
    *,
    list_serializer:        type[T] | None = None,
    retrieve_serializer:    type[T] | None = None,
    create_serializer:      type[T] | None = None,
    fallback_serializer:    type[T]
) -> Callable[..., T]:

    _safe = partial(_fall_back, fallback=fallback_serializer)

    def get_serializer_class(action: Action) -> type[T]:
        serializer_class: type[T] = fallback_serializer

        match action:
            case Action.LIST: serializer_class = _safe(list_serializer)
            case Action.RETRIEVE: serializer_class = _safe(retrieve_serializer)
            case Action.CREATE: serializer_class = _safe(create_serializer)
            case _: serializer_class = fallback_serializer

        return serializer_class


    return partial(
        _construct_serializer,
        get_serializer_class=get_serializer_class
    )
