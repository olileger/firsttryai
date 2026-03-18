import os
from src import AgentHelper
from src import FileHelper
from src import ModelHelper
from src.Team import Team
from src.TeamOpenAIAgentSDK import TeamOpenAIAgentSDK


async def createTeam(filePath: str, tracing: frozenset[str] | None = None) -> Team:
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
                agents.append(await AgentHelper.createAgent(a["file"], tracing=tracing))
            else:
                raise Exception(f"Agent {a} is not a valid YAML as it miss the 'file' key.")

        # Model: read the API Key from the environment variable if needed.
        model_def = FileHelper.interpretYamlModelObject(file["model"])
        model = ModelHelper.createModel(model_def["name"], model_def["provider"], model_def["api-key"])

        sdk = os.getenv("SDK")
        if sdk == "OpenAI Agent SDK":
            team_class = TeamOpenAIAgentSDK
        elif sdk == "Microsoft Agent Framework":
            raise NotImplementedError("SDK 'Microsoft Agent Framework' is not implemented yet.")
        else:
            raise ValueError(f"Unsupported SDK: {sdk}")

        return team_class(
            name=file["name"],
            agents=agents,
            model=model,
            manager_prompt=file["prompt"],
            max_turns=int(file["termination"].get("max-turns", 10)),
            tracing=tracing
        )
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")
