import logging

logging.basicConfig(level= logging.DEBUG)


class Storage:

    _storage = {}

    def __init__(self): pass

    @classmethod
    def have_message(cls, uuid):
        try:
            _ = cls._storage[uuid]
            return True
        except Exception as e:
            # logging.info("ERROR ON GETTING FROM STORAGE" % str(e))
            return False

    @classmethod
    def get_message(cls, uuis):
        return cls._storage[uuid]

    @classmethod
    def add_message(cls, uuid, message):
        logging.info("ADD MESSAGE TO STORAGE")
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
