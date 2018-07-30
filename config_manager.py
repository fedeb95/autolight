import json

class ConfigManager:

    instance=None

    def __init__(self,config_name):
        with open(config_name) as config:
            self.config = json.load(config)
    
    @staticmethod
    def get_instance(config_name=None):
        if ConfigManager.instance == None: 
            if config_name == None:
                raise ValueError('No config file provided!')
            ConfigManager.instance = ConfigManager(config_name)
        return ConfigManager.instance
