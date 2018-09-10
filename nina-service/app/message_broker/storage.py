class Storage:

    _storage = {}

    @classmethod
    def have_message(cls, uuid):
        try:
            _ = cls._storage[uui]
            return True
        except Exception as e:
            return False

    @classmethod
    def get_message(cls, uuis):
        return cls._storage[uuid]

    @classmethod
    def add_message(cls, uuid, message):
        cls._storage[uuid] = message

    @classmethod
    def remove_message(cls, uuid):
        del cls._storage[uuid]
