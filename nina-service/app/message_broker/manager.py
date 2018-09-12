class Manager:

    def __init__(self):
        self._methods_dict = {}

        for klass in self.__class__.__subclasses__():
            for method_name in dir(klass):
                if method_name[0] == '_':
                    continue
                setattr(self.__class__, method_name, getattr(klass, method_name))
                self._methods_dict[method_name] = True

    def run_method(self, method_name, kwargs= {}):
        try:
            self._methods_dict[method_name]
            return getattr(self, method_name)(**kwargs)
        except Exception as e:
            return False
