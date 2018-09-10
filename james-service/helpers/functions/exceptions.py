class AppInitializedError(Exception):
    def __init__(self, dErrorArguments):
        Exception.__init__(self,"App %s already initialized" % dErrorArguments)
        self.dErrorArguments = dErrorArguments