import yaml

with open (r"v1\Assobio\CONFIG_MODELS.yaml", "r", encoding = "utf-8") as file:
    config = yaml.safe_load (file)


print (config["MODELS"].keys())


