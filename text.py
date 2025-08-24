import json
import yaml

stuff = yaml.safe_load(open("text.yaml").read())
print(stuff)