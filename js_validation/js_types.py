
class JsError(Exception):

    def __init__(self, value):
        super(JsError, self).__init__('invalid')
        self.json = value


class JsValue(object):
    
    python_type = (str, unicode, int, long, float, bool, list, dict, None,)

    def __init__(self, **kwargs):
        self.tests = []
        self.fixes = []
        self.is_optional = kwargs.get('optional', False)
        self.may_be_null = kwargs.get('null', False)
        self.has_default = False
        self.default_value = None
        
        if kwargs.has_key('test'):
            tests = kwargs['test']
            if not isinstance(tests, list):
                tests = [tests]
            for t in tests:
                if not callable(t):
                    raise ValueError('test is not callable')
                self.tests.append(t)

        if kwargs.has_key('fix'):
            fixes = kwargs['fix']
            if not isinstance(fixes, list):
                fixes = [fixes]
            for f in fixes:
                if not callable(f):
                    raise ValueError('test is not callable')
                self.fixes.append(f)
        
        if kwargs.has_key('default'):
            if not isinstance(kwargs['default'], JsValue.python_type):
                raise ValueError('default is not a json type')
            self.has_default = True
            self.default_value = kwargs['default']


    def validate(self, value):
        if self.may_be_null and value is None:
            return None

        for fix in self.fixes:
            value = fix(value)

        if not isinstance(value, self.python_type):
            raise JsError('invalid type')
        
        for test in self.tests:
            test(value)

        return value
 

class JsString(JsValue):

    python_type = (str, unicode,)


class JsInt(JsValue):
    
    python_type = int


class JsLong(JsValue):
    
    python_type = long


class JsFloat(JsValue):
    
    python_type = float


class JsBool(JsValue):
    
    python_type = bool


class JsNull(JsValue):
    
    python_type = None


class JsArray(JsValue):

    python_type = list

    def __init__(self, **kwargs):
        super(JsArray, self).__init__(**kwargs)
        self.item_type = None


    def item(self, js_type):
        if not isinstance(js_type, JsValue):
            raise ValueError('item is not JsValue')
        self.item_type = js_type
        return self


    def model(self, js_types):
        self.item_type = []
        for js_type in js_types:
            if not isinstance(js_type, JsValue):
                raise ValueError('item is not JsValue')
            self.item_type.append(js_type)
        return self


    def validate(self, value):
        value = super(JsArray, self).validate(value)

        if self.item_type is None or value is None:
            return value

        cleaned = []
        errors = []
        index = 0

        if isinstance(self.item_type, JsValue):
            
            for item in value:
                try:
                    cleaned.append(self.item_type.validate(item))
                except JsError, inst:
                    errors.append({'index': index, 'error': inst.json})
                index += 1
        
        else:
            
            for item_type in self.item_type:
                try:
                    cleaned.append(item_type.validate(value[index]))
                except IndexError:
                    if item_type.has_default:
                        cleaned.append(value_type.default_value)
                    elif not value_type.is_optional:
                        errors.append({'index': index, 'error': 'missing'})
                except JsError, inst:
                    errors.append({'index': index, 'error': inst.json})
                index += 1

        if errors:
            raise JsError(errors)

        return cleaned


class JsObject(JsValue):

    python_type = dict

    def __init__(self, **kwargs):
        super(JsObject, self).__init__(**kwargs)
        self.value_types = None

    def _set_value_types(self, model):
        for value_type in model.values():
            if not isinstance(value_type, JsValue):
                raise ValueError('value is not JsValue')
        self.value_types = model


    def model(self, model):
        self._set_value_types(model)
        return self
        

    def keys(self, **kwargs):
        self._set_value_types(kwargs)
        return self


    def validate(self, value):
        value = super(JsObject, self).validate(value)

        if not self.value_types or value is None:
            return value

        cleaned = {}
        errors = {}

        for key, value_type in self.value_types.items():
            try:
                cleaned[key] = value_type.validate(value[key])
            except KeyError:
                if value_type.has_default:
                    cleaned[key] = value_type.default_value
                elif not value_type.is_optional:
                    errors[key] = 'missing'
            except JsError, inst:
                errors[key] = inst.json

        if errors:
            raise JsError(errors)

        return cleaned















