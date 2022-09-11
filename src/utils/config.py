import json
import yaml


def load_config(config_name: str):
    with open(config_name, 'r') as f:
        return json.load(f)


def save_config(config, config_name: str):
    with open(config_name, 'w') as f:
        json.dump(config, f)
        
def load_yaml_config(config_name: str):
    with open(config_name, 'r') as f:
        return yaml.safe_load(f)

def save_yaml_config(config, config_name: str):
    with open(config_name, 'w') as f:
        yaml.safe_dump(config, f, sort_keys=False)


def load_properties(file_path: str) -> dict:
    properties = {}
    with open(file_path, 'r') as properties_file:
        for line in properties_file:
            if line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            properties[key] = value.strip()
    return properties