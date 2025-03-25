import os
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from ag_Ext_Models import ModelHelper


class TeamHelper:

    def CreateTeam(agents,
                   systemMessageFilePath,
                   apikeyEnvVarName,
                   model = "4o",
                   termination_condition = TextMentionTermination("## END ##"),
                   max_turns = 10):

        with open(systemMessageFilePath, 'r') as file:
            systemMessage = file.read()

        return SelectorGroupChat(participants=agents,
                                 model_client=ModelHelper.CreateModel(model, apikeyEnvVarName),
                                 selector_prompt=systemMessage,
                                 termination_condition=termination_condition,
                                 max_turns=max_turns)