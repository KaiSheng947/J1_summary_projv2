"""Game configuration management and import."""

import yaml

with open("text.yaml", "r") as file:
    _data = yaml.safe_load(file)

player_data = _data["player_data"]
rooms = _data["rooms"]
text = _data["text"]
