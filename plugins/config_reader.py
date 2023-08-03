import yaml


config_file = "./configs/config.yml"


def read_config(category:str = "$all", filepath: str = config_file):
    with open(filepath, 'r', encoding="utf-8") as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    if category == "$all":
        return result
    else:
        if category not in result:
            return {}    
        else:
            return result[category]
