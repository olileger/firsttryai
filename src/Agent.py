from agents import Agent as OpenAIAgent, Runner
from src.Model import Model


class Agent:
    """Wrap an OpenAI Agent SDK agent."""

    def __init__(self, name: str, instruction: str, model: Model):
        self._name = name
        self._instruction = instruction
        self._agent = OpenAIAgent(
            name=self._name,
            instructions=self._instruction,
            model=model.getUnderlyingModel()
        )

    async def run(self, task: str):
        return await Runner.run(self._agent, task)
    
    def getUnderlyingAgent(self):
        return self._agent
