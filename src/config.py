import configparser

class AutoConfig:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.optionxform = str 
        self.config.read(file_path)

    @property
    def USE_AUTO_FARM(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'USE_AUTO_FARM')

    @property
    def EARN_DIAMONDS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'EARN_DIAMONDS_ENABLED')

    @property
    def EARN_DIAMOND_BREAKABLES_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'EARN_DIAMOND_BREAKABLES_ENABLED')

    @property
    def HATCH_BEST_EGGS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'HATCH_BEST_EGGS_ENABLED')

    @property
    def BREAK_BREAKABLES_BEST_AREA_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'BREAK_BREAKABLES_BEST_AREA_ENABLED')

    @property
    def USE_IV_POTIONS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'USE_IV_POTIONS_ENABLED')

    @property
    def USE_FRUITS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'USE_FRUITS_ENABLED')

    @property
    def BREAK_MINI_CHESTS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'BREAK_MINI_CHESTS_ENABLED')

    @property
    def BREAK_COIN_JARS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'BREAK_COIN_JARS_ENABLED')

    @property
    def BREAK_COMETS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'BREAK_COMETS_ENABLED')

    @property
    def BREAK_PINATAS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'BREAK_PINATAS_ENABLED')

    @property
    def BREAK_LUCKY_BLOCKS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'BREAK_LUCKY_BLOCKS_ENABLED')

    @property
    def HATCH_RARE_PETS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'HATCH_RARE_PETS_ENABLED')

    @property
    def CONSUME_XP_POTIONS_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean('Enabled/Disabled', 'CONSUME_XP_POTIONS_ENABLED')

    @property
    def XP_POTION(self):
        self.config.read(self.file_path)
        return self.config.get('Consume XP Potions', 'XP_POTION')

    @property
    def MAXIMUM_XP_POTION_USAGE(self):
        self.config.read(self.file_path)
        return self.config.getint('Consume XP Potions', 'MAXIMUM_XP_POTION_USAGE')

    @property
    def FRUITS(self):
        self.config.read(self.file_path)
        return [fruit.strip() for fruit in self.config.get('Use Fruits', 'FRUITS').split(',')]

    @property
    def MAXIMUM_FRUIT_USAGE_EACH(self):
        self.config.read(self.file_path)
        return self.config.getint('Use Fruits', 'MAXIMUM_FRUIT_USAGE_EACH')

    @property
    def IV_POTION(self):
        self.config.read(self.file_path)
        return self.config.get('Use Potion IV', 'IV_POTION')

    @property
    def MAXIMUM_POTION_USAGE(self):
        self.config.read(self.file_path)
        return self.config.getint('Use Potion IV', 'MAXIMUM_POTION_USAGE')

    @property
    def NO_QUEST_CHECK_INERVAL(self):
        self.config.read(self.file_path)
        return self.config.getint('Delays (in Seconds)', 'NO_QUEST_CHECK_INERVAL')

    @property
    def ACTIVE_CHECK_INTERVAL(self):
        self.config.read(self.file_path)
        return self.config.getint('Delays (in Seconds)', 'ACTIVE_CHECK_INTERVAL')

    @property
    def TELEPORT_DELAY(self):
        self.config.read(self.file_path)
        return self.config.getint('Delays (in Seconds)', 'TELEPORT_DELAY')

    @property
    def X_OFFSET(self):
        self.config.read(self.file_path)
        return self.config.getint('Offsets', 'X')

    @property
    def Y_OFFSET(self):
        self.config.read(self.file_path)
        return self.config.getint('Offsets', 'Y')
    
    @property
    def POTION_USE_DELAY(self):
        self.config.read(self.file_path)
        return self.config.getint('Spawn Delays (in Seconds)', 'POTION_USE_DELAY')

    @property
    def COIN_JAR_SPAWN_DELAY(self):
        self.config.read(self.file_path)
        return self.config.getint('Spawn Delays (in Seconds)', 'COIN_JAR_SPAWN_DELAY')

    @property
    def LUCKY_BLOCK_SPAWN_DELAY(self):
        self.config.read(self.file_path)
        return self.config.getint('Spawn Delays (in Seconds)', 'LUCKY_BLOCK_SPAWN_DELAY')

    @property
    def PINATA_SPAWN_DELAY(self):
        self.config.read(self.file_path)
        return self.config.getint('Spawn Delays (in Seconds)', 'PINATA_SPAWN_DELAY')

    @property
    def COMET_SPAWN_DELAY(self):
        self.config.read(self.file_path)
        return self.config.getint('Spawn Delays (in Seconds)', 'COMET_SPAWN_DELAY')
    
    @property
    def MACRO_ENABLED(self):
        self.config.read(self.file_path)
        return self.config.getboolean("Developer (Do Not Modify)", "MACRO_ENABLED")

    @MACRO_ENABLED.setter
    def MACRO_ENABLED(self, value):
        self.config.set("Developer (Do Not Modify)", "MACRO_ENABLED", str(value))
        with open(self.file_path, 'w') as config_file:
            self.config.write(config_file)
            
    @property
    def SYSTEM_RUNNING(self):
        self.config.read(self.file_path)
        return self.config.getboolean("Developer (Do Not Modify)", "SYSTEM_RUNNING")

    @SYSTEM_RUNNING.setter
    def SYSTEM_RUNNING(self, value):
        self.config.set("Developer (Do Not Modify)", "SYSTEM_RUNNING", str(value))
        with open(self.file_path, 'w') as config_file:
            self.config.write(config_file)

config_path = 'config.ini'