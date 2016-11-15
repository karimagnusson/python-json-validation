from js_types import JsError
from django.core.validators import validate_email


def max_length(limit):
    def tester(value):
        if len(value) > limit:
            raise JsError('max length %d' % limit)
    return tester


def min_length(limit):
    def tester(value):
        if len(value) < limit:
            raise JsError('min length %d' % limit)
    return tester


def length(length):
    def tester(value):
        if len(value) != length:
            raise JsError('length must be %d' % length)
    return tester


def length_range(f, t):
    def tester(value):
        if len(value) < f:
            raise JsError('min length %d' % f)
        if len(value) > t:
            raise JsError('max length %d' % t)
    return tester


def empty_or_length(length):
    def tester(value):
        if len(value) not in (0, length,):
            raise JsError('length must be %d' % length)
    return tester


def is_numeric(value):
    if not value.isdigit():
        raise JsError('invalid')


def not_zero(value):
    if value == 0:
        raise JsError('zero not allowed')


def has_length(value):
    if not len(value):
        raise JsError('empty')


def email(value):
    try:
        validate_email(value)
    except:
        raise JsError('invalid')


def optional_email(value):
    if len(value):
        email(value)


