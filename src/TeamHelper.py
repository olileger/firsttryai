from autogen_agentchat.teams import SelectorGroupChat
from AgentHelper import createAgent
from FileHelper import readYamlFile, interpretYamlModelObject
from ModelHelper import createModel


async def createTeam(filePath: str) -> SelectorGroupChat:
    """
    Creates a team of agents for group chat.
    :param agents: List of agents to be included in the team.
    :param systemMessageFilePath: Path to the YAML file containing the team config.
    """
    file = readYamlFile(filePath)
    try:
        # Agents: load the YAML files for each agent
        for a in file["agents"]:
            if isinstance(a, dict) and "file" in a:
                a["object"] = await createAgent(a["file"])
            else:
                raise Exception(f"Agent {a} is not a valid YAML as it miss the 'file' key.")
            
        file["agents"] = [a["object"] for a in file["agents"]]

        # Model: read the API Key from the environment variable if needed.
        file["model"] = interpretYamlModelObject(file["model"])
        
        return SelectorGroupChat(participants=file["agents"],
                                    model_client=createModel(file["model"]["name"], file["model"]["provider"], file["model"]["api-key"]),
                                    selector_prompt=file["prompt"],
                                    termination_condition=file["termination"]["keyword"],
                                    max_turns=file["termination"]["max-round"])
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")