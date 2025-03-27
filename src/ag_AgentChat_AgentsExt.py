from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from ag_Ext_Models import ModelHelper
from tool_FileHelper import FileHelper


#
# AgentHelper
# This class is used to create agents for the AgentChat framework.
#
class AgentHelper:

    @staticmethod
    async def CreateAgent(filePath: str) -> AssistantAgent:
        file = FileHelper.readYamlFile(filePath)
        try:
            # Check if description exists in the dictionary
            if "description" not in file or file["description"] == "":
                model = FileHelper.interpretYamlModelObject(file["model"])
                llm = ModelHelper.CreateModel(model["name"], model["provider"], model["api-key"])
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