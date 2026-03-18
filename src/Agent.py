from typing import Any
from agents import Agent as OpenAIAgent, Runner
from agents.agent_tool_input import AgentAsToolInput
from src.Model import Model
from src.Tracing import create_stdout_agent_hooks


class Agent:
    """Wrap an OpenAI Agent SDK agent."""

    def __init__(
        self,
        name: str,
        instruction: str,
        model: Model,
        description: str | None = None,
        tools: list[Any] | None = None,
        tracing: frozenset[str] | None = None
    ):
        self._name = name
        self._instruction = instruction
        self._description = description.strip() if description else self._inferDescription(instruction, name)
        self._agent = OpenAIAgent(
            name=self._name,
            instructions=self._instruction,
            tools=[] if tools is None else tools,
            model=model.getUnderlyingModel(),
            hooks=create_stdout_agent_hooks(tracing)
        )

    async def run(self, task: str, max_turns: int | None = None):
        runner_args = {}
        if max_turns is not None:
            runner_args["max_turns"] = max_turns
        return await Runner.run(self._agent, task, **runner_args)

    def getName(self):
        return self._name

    def getInstruction(self):
        return self._instruction

    def getDescription(self):
        return self._description

    def getUnderlyingAgent(self):
        return self._agent

    def asTool(self):
        return self._agent.as_tool(
            tool_name=self.getName().replace(" ", "_").lower(),
            tool_description=self.getDescription(),
            parameters=AgentAsToolInput
        )

    @staticmethod
    def _inferDescription(instruction: str, fallback: str) -> str:
        for line in instruction.splitlines():
            candidate = line.strip()
            if candidate:
                return candidate
        return fallback
