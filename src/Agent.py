from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


class Agent:
    """Provide abstraction for an Agent for an easy library switching."""
    
    def __init__(self, name: str, instruction: str, model_client: OpenAIChatCompletionClient):
        self._name = name
        self._instruction = instruction
        self._agent = AssistantAgent(
            name=self._name,
            system_message=self._instruction,
            model_client=model_client
        )
    
    def run(self, task: str):
        return self._agent.run_stream(task=task)
