import logging

logging.basicConfig(level= logging.INFO)

class Manager:

    def __init__(self):
        self._methods_dict = {}

        logging.info("INIT MANAGER: %s" % str(self.__class__.__subclasses__()))

        for klass in self.__class__.__subclasses__():
            for method_name in dir(klass):
                if method_name[0] == '_':
                    continue
                setattr(self.__class__, method_name, getattr(klass, method_name))
                self._methods_dict[method_name] = True

    def run_function(self, method_name, kwargs= {}):
        logging.info("-------- list of methods --------")
        logging.info(self._methods_dict)
        try:
            self._methods_dict[method_name]
            return getattr(self, method_name)(**kwargs)
        except Exception as e:
            return False
