from src import FileHelper, ModelHelper
from src.Agent import Agent


async def createAgent(filePath: str) -> Agent:
    file = FileHelper.readYamlFile(filePath)
    try:
        model = FileHelper.interpretYamlModelObject(file["model"])
        model_client = ModelHelper.createModel(model["name"], model["provider"], model["api-key"])
        return Agent(name=file["name"], instruction=file["prompt"], model_client=model_client)
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")