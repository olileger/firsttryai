from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from ag_Ext_Models import ModelHelper


#
# AgentHelper
# This class is used to create agents for the AgentChat framework.
#
class AgentHelper:

    async def CreateAgent(name, systemMessageFilePath, apikeyEnvVarName, description = "", model = "4o"):
        with open(systemMessageFilePath, 'r') as file:
            systemMessage = file.read()

        if description == "":
            llm = ModelHelper.CreateModel(model, apikeyEnvVarName)
            description = await llm.create([UserMessage(content=F"Describe the following prompt message in 1 short sentence: {systemMessage}",
                                                        source="user")])

        return AssistantAgent(name=name,
                              description=description.content,
                              system_message=systemMessage,
                              model_client=ModelHelper.CreateModel(model, apikeyEnvVarName))