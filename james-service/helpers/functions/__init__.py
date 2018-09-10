import importlib

def get_config_by_env(env):
    config = importlib.import_module('src.settings.%s' % env)
    config_list = {}
    [config_list.update({key : getattr(config, key)}) for key in dir(config) if str(key)[0] != '_']
    return config_list