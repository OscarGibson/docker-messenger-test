from .exceptions import AppInitializedError

class UrlRules:

    app = None

    class _RulesObject:

        def __init__(self, prefix, app):
            self.prefix = prefix
            self._app = app

        def add(self, name, **kwargs):
            self._app.add_url_rule(self.prefix + name, **kwargs)

    def __init__(self, app= None):
        if app:
            self.add_app(app)

    def init_app(self, app):
        self.add_app(app)

    @classmethod
    def create_rules_object(cls, prefix):
        return cls._RulesObject(prefix, cls.app)

    @classmethod
    def add_app(cls, app):
        cls.app = app
        # if cls.app:
        #   raise AppInitializedError(cls.app.name)
        # else:
        #   cls.app = app