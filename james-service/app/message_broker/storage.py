class Storage:

    _storage = {}

    def __init__(self): pass

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
    def update_message(cls, messages):
        cls._storage.update(messages)

    @classmethod
    def remove_message(cls, uuid):
        del cls._storage[uuid]

    @classmethod
    def reset(cls):
        cls._storage = {}
