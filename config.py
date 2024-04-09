import configparser

config = configparser.ConfigParser()
config.read('config.ini')

USE_AUTO_FARM = config.getboolean('Enabled/Disabled', 'USE_AUTO_FARM')

EARN_DIAMONDS_ENABLED = config.getboolean('Enabled/Disabled', 'EARN_DIAMONDS_ENABLED')
EARN_DIAMOND_BREAKABLES_ENABLED = config.getboolean('Enabled/Disabled', 'EARN_DIAMOND_BREAKABLES_ENABLED')
HATCH_BEST_EGGS_ENABLED = config.getboolean('Enabled/Disabled', 'HATCH_BEST_EGGS_ENABLED')
BREAK_BREAKABLES_BEST_AREA_ENABLED = config.getboolean('Enabled/Disabled', 'BREAK_BREAKABLES_BEST_AREA_ENABLED')
USE_IV_POTIONS_ENABLED = config.getboolean('Enabled/Disabled', 'USE_IV_POTIONS_ENABLED')
USE_FRUITS_ENABLED = config.getboolean('Enabled/Disabled', 'USE_FRUITS_ENABLED')
BREAK_MINI_CHESTS_ENABLED = config.getboolean('Enabled/Disabled', 'BREAK_MINI_CHESTS_ENABLED')
BREAK_COIN_JARS_ENABLED = config.getboolean('Enabled/Disabled', 'BREAK_COIN_JARS_ENABLED')
BREAK_COMETS_ENABLED = config.getboolean('Enabled/Disabled', 'BREAK_COMETS_ENABLED')
BREAK_PINATAS_ENABLED = config.getboolean('Enabled/Disabled', 'BREAK_PINATAS_ENABLED')
BREAK_LUCKY_BLOCKS_ENABLED = config.getboolean('Enabled/Disabled', 'BREAK_LUCKY_BLOCKS_ENABLED')
HATCH_RARE_PETS_ENABLED = config.getboolean('Enabled/Disabled', 'HATCH_RARE_PETS_ENABLED')
CONSUME_XP_POTIONS_ENABLED = config.getboolean('Enabled/Disabled', 'CONSUME_XP_POTIONS_ENABLED')

XP_POTION = config.get('Consume XP Potions', 'XP_POTION')
MAXIMUM_XP_POTION_USAGE = config.getint('Consume XP Potions', 'MAXIMUM_XP_POTION_USAGE')

FRUITS = [fruit.strip() for fruit in config.get('Use Fruits', 'FRUITS').split(',')]
MAXIMUM_FRUIT_USAGE_EACH = config.getint('Use Fruits', 'MAXIMUM_FRUIT_USAGE_EACH')

IV_POTION = config.get('Use Potion IV', 'IV_POTION')
MAXIMUM_POTION_USAGE = config.getint('Use Potion IV', 'MAXIMUM_POTION_USAGE')

ITEM_SPAWN_DELAY = config.getint('Delays (in Seconds)', 'ITEM_SPAWN_DELAY')
ACTIVE_CHECK_INTERVAL = config.getint('Delays (in Seconds)', 'ACTIVE_CHECK_INTERVAL')
TELEPORT_DELAY = config.getint('Delays (in Seconds)', 'TELEPORT_DELAY')

X_OFFSET = config.getint('Offsets', "X")
Y_OFFSET = config.getint('Offsets', "Y")