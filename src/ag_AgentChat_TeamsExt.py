from autogen_agentchat.teams import SelectorGroupChat
from ag_AgentChat_AgentsExt import AgentHelper
from ag_Ext_Models import ModelHelper
from tool_FileHelper import FileHelper


class TeamHelper:

    @staticmethod
    async def CreateTeam(filePath: str) -> SelectorGroupChat:
        """
        Creates a team of agents for group chat.
        :param agents: List of agents to be included in the team.
        :param systemMessageFilePath: Path to the YAML file containing the team config.
        """
        file = FileHelper.readYamlFile(filePath)
        try:
            # Agents: load the YAML files for each agent
            for a in file["agents"]:
                if isinstance(a, dict) and "file" in a:
                    a["object"] = await AgentHelper.CreateAgent(a["file"])
                else:
                    raise Exception(f"Agent {a} is not a valid YAML as it miss the 'file' key.")
                
            file["agents"] = [a["object"] for a in file["agents"]]

            # Model: read the API Key from the environment variable if needed.
            file["model"] = FileHelper.interpretYamlModelObject(file["model"])
            
            return SelectorGroupChat(participants=file["agents"],
                                     model_client=ModelHelper.CreateModel(file["model"]["name"], file["model"]["provider"], file["model"]["api-key"]),
                                     selector_prompt=file["prompt"],
                                     termination_condition=file["termination"]["keyword"],
                                     max_turns=file["termination"]["max-round"])
        except KeyError as e:
            raise Exception(f"YAML file doesn't contains key: {e}")