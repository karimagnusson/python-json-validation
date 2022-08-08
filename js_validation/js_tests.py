# Copyright 2021 Kari Magnusson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from js_types import JsError


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




