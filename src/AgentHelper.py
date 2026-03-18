import os
from src import FileHelper, ModelHelper
from src.Agent import Agent
from src.AgentOpenAIAgentSDK import AgentOpenAIAgentSDK


async def createAgent(filePath: str, tracing: frozenset[str] | None = None) -> Agent:
    file = FileHelper.readYamlFile(filePath)
    try:
        model_def = FileHelper.interpretYamlModelObject(file["model"])
        model = ModelHelper.createModel(model_def["name"], model_def["provider"], model_def["api-key"])
        
        sdk = os.getenv("SDK")
        if sdk == "OpenAI Agent SDK":
            agent_class = AgentOpenAIAgentSDK
        elif sdk == "Microsoft Agent Framework":
            raise NotImplementedError("SDK 'Microsoft Agent Framework' is not implemented yet.")
        else:
            raise ValueError(f"Unsupported SDK: {sdk}")

        return agent_class(
            name=file["name"],
            instruction=file["prompt"],
            model=model,
            description="" if not file.get("description") else file["description"],
            tracing=tracing
        )
    except KeyError as e:
        raise Exception(f"YAML file doesn't contains key: {e}")
