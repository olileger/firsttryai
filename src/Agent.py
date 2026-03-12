from agents import Agent as OpenAIAgent, Runner
from src.Model import Model


class Agent:
    """Wrap an OpenAI Agent SDK agent."""

    def __init__(self, name: str, instruction: str, model: Model, description: str | None = None):
        self._name = name
        self._instruction = instruction
        self._description = description.strip() if description else self._inferDescription(instruction, name)
        self._agent = OpenAIAgent(
            name=self._name,
            instructions=self._instruction,
            model=model.getUnderlyingModel()
        )

    async def run(self, task: str):
        return await Runner.run(self._agent, task)

    def getName(self):
        return self._name

    def getInstruction(self):
        return self._instruction

    def getDescription(self):
        return self._description

    def getUnderlyingAgent(self):
        return self._agent

    @staticmethod
    def _inferDescription(instruction: str, fallback: str) -> str:
        for line in instruction.splitlines():
            candidate = line.strip()
            if candidate:
                return candidate
        return fallback
