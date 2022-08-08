from js_validation.js_types import *


data1 = {
    'string': 'foo',
    'int': 3,
    'long': 4L,
    'float': 1.2,
    'bool': True,
    'list': [1, 2, 3],
    'dict': {
        'int': 1,
        'bool': False
    }
}

model1 = JsObject().model({
    'string': JsString(),
    'int': JsInt(),
    'long': JsLong(),
    'float': JsFloat(),
    'bool': JsBool(),
    'list': JsArray().item(JsInt()),
    'dict': JsObject().model({
        'int': JsInt(),
        'bool': JsBool()
    })
})

try:
    model1.validate(data1)
    print 'Ok'
except JsError, inst:
    print inst.json