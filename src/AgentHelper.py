from src import FileHelper
from src.Agent import Agent


async def createAgent(filePath: str) -> Agent:
    file = FileHelper.readYamlFile(filePath)
    try:
        a = Agent(name=file["name"], instruction=file["prompt"], model=file["model"])
        return a
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")