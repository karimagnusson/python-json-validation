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