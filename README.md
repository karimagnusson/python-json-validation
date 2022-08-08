## Python JSON Validation



#### Example 1
```python
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
```

#### Example 2
```python
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
```


#### Example 3
```python
import json
from js_validation.js_types import *
from js_validation.js_tests import length
from js_validation.js_fixes import strip

data3 = {
    'name': '  Joe  ',
    'age': None,
    'country': 'US',
    'city': None
}

model3 = JsObject().model({
    'name': JsString(fix=[strip]),
    'age': JsInt(default=35),
    'country': JsString(test=[length(2)]),
    'city': JsString(null=True),
    'phone': JsInt(optional=True)
})

try:
    cleaned = model3.validate(data3)
    print(json.dumps(cleaned, indent=4))
except JsError, inst:
    print json.dumps(inst.json)
```





