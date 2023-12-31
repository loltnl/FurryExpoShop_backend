import yaml


def read_config(category:str = "$all", filepath: str = "./configs/config.yml") -> dict:
    with open(file=filepath, mode='r', encoding="utf-8") as f:
        result = yaml.load(stream=f.read(), Loader=yaml.FullLoader)
    if category == "$all":
        return result
    else:
        if category not in result:
            return {}    
        else:
            result = result[category]
            return result
