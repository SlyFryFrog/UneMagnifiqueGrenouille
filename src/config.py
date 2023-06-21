import json

json_file = "resources/settings.json"


def default_config():
    '''Returns the default guild configuration'''
    guild_config = {
        "subscribe.daily": {
            "enabled": False,
            "channel.id": None
        },
        "channel.access": {
            "limited": False,
            "channel.id": [

            ]
        }
    }
        
    return guild_config


def update_guild_settings(guild_id_list):
    '''Updates the channel saved for the daily frog fact'''
    with open(json_file, "w") as file:
        json.dump(guild_id_list, file, indent=4, separators=(',', ': '))


def read_config():
    with open(json_file, "r") as file:
        guild_id_list = json.load(file)
        
    return guild_id_list
