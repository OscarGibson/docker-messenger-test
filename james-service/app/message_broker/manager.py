import collections

class Manager:

    class __metaclass__(type):
        __inheritors__ = collections.defaultdict(list)

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            for base in klass.mro()[1:-1]:
                meta.__inheritors__[base].append(klass)
            return klass

    @classmethod
    def run_function(cls, question):
    	return str(dir(cls))