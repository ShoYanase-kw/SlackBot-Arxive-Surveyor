import yaml

def load_from_yml(path):
    with open(path) as file:
        config = yaml.safe_load(file)
        return config