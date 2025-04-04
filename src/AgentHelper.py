from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from src import FileHelper
from src import ModelHelper


async def createAgent(filePath: str) -> AssistantAgent:
    file = FileHelper.readYamlFile(filePath)
    try:
        # Check if description exists in the dictionary
        if "description" not in file or file["description"] == "":
            model = FileHelper.interpretYamlModelObject(file["model"])
            llm = ModelHelper.createModel(model["name"], model["provider"], model["api-key"])
            description = await llm.create([UserMessage(content=F"Describe the following prompt message in 1 short sentence: {file["prompt"]}",
                                                        source="user")])
            description = description.content
        else:
            description = file["description"]

        return AssistantAgent(name=file["name"],
                                description=description,
                                system_message=file["prompt"],
                                model_client=llm)
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")