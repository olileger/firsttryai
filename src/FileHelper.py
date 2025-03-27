import os
import yaml


def readYamlFile(filePath):
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param filePath: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"File not found: {filePath}")
    
    with open(filePath, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise Exception(f"Error reading YAML file: {e}")
        
@staticmethod
def interpretYamlModelObject(yamlModel):
    """
    Interprets the YAML model object and replaces any environment variable references with their actual values.
    """
    apikey = yamlModel["api-key"]
    if isinstance(apikey, str) and apikey.lower().startswith("env:"):
        apikey = apikey[4:]
        yamlModel["api-key"] = os.getenv(apikey)
    return yamlModel