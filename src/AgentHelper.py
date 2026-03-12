from src import FileHelper, ModelHelper
from src.Agent import Agent


async def createAgent(filePath: str) -> Agent:
    file = FileHelper.readYamlFile(filePath)
    try:
        model_def = FileHelper.interpretYamlModelObject(file["model"])
        model = ModelHelper.createModel(model_def["name"], model_def["provider"], model_def["api-key"])
        return Agent(
            name=file["name"],
            instruction=file["prompt"],
            model=model,
            description="" if not file.get("description") else file["description"]
        )
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")