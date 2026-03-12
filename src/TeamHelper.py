from src import AgentHelper
from src import FileHelper
from src import ModelHelper
from src.Team import Team


async def createTeam(filePath: str) -> Team:
    """
    Creates a manager agent coordinating participant agents.
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
        model_def = FileHelper.interpretYamlModelObject(file["model"])
        model = ModelHelper.createModel(model_def["name"], model_def["provider"], model_def["api-key"])

        return Team(
            name=file["name"],
            agents=agents,
            model=model,
            manager_prompt=file["prompt"],
            max_turns=int(file["termination"].get("max-turns", 10))
        )
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")
