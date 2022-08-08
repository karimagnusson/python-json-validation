from js_validation.js_types import *


data2 = {
    'dict': {
        'list': [
            {
                'float': 1.2,
                'bool': True
            }
        ],
        'dict': {
            'string': 'foo',
            'list': [1, 2, 3]
        }
    }
}

model2 = JsObject().model({
    'dict': JsObject().model({
        'list': JsArray().item(JsObject().model({
            'float': JsFloat(),
            'bool': JsBool()
        })),
        'dict': JsObject().model({
            'string': JsString(),
            'list': JsArray().item(JsInt())
        })
    })
})

try:
    model2.validate(data2)
    print 'Ok'
except JsError, inst:
    print inst.json