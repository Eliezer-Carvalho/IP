import yaml

with open (r"v1\Assobio\modelos_config.yaml", "r", encoding = "utf-8") as file:
    config = yaml.safe_load (file)


print (config["MODELS"])

