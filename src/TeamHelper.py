from src import AgentHelper
from src import FileHelper
from src import ModelHelper
from src.Team import Team


async def createTeam(filePath: str) -> Team:
    """
    Creates a team of agents for group chat.
    :param filePath: Path to the YAML file containing the team config.
    """
    file = FileHelper.readYamlFile(filePath)
    try:
        # Agents: load the YAML files for each agent
        agents = []
        for a in file["agents"]:
            if isinstance(a, dict) and "file" in a:
                agents.append(await AgentHelper.createAgent(a["file"]))
            else:
                raise Exception(f"Agent {a} is not a valid YAML as it miss the 'file' key.")

        # Model: read the API Key from the environment variable if needed.
        model = FileHelper.interpretYamlModelObject(file["model"])
        model_client = ModelHelper.createModel(model["name"], model["provider"], model["api-key"]).client

        return Team(
            name=file["name"],
            agents=agents,
            model_client=model_client,
            selector_prompt=file["prompt"],
            max_round=int(file["termination"]["max-round"]),
            termination_keyword=file["termination"]["keyword"]
        )
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")
