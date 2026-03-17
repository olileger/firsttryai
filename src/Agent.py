from typing import Any
from agents import Agent as OpenAIAgent, Runner, handoff
from src.Model import Model
from src.Tracing import create_stdout_agent_hooks
from src.Tracing import TRACE_AGENT


class Agent:
    """Wrap an OpenAI Agent SDK agent."""

    def __init__(
        self,
        name: str,
        instruction: str,
        model: Model,
        description: str | None = None,
        tools: list[Any] | None = None,
        handoffs: list[Any] | None = None,
        tracing: frozenset[str] | None = None
    ):
        self._name = name
        self._instruction = instruction
        self._description = description.strip() if description else self._inferDescription(instruction, name)
        self.tracing = frozenset() if tracing is None else tracing
        self._agent = OpenAIAgent(
            name=self._name,
            instructions=self._instruction,
            tools=[] if tools is None else tools,
            handoffs=[] if handoffs is None else handoffs,
            model=model.getUnderlyingModel(),
            hooks=create_stdout_agent_hooks(self.tracing)
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

    def updateInstruction(self, instruction: str):
        self._instruction = instruction
        self._agent.instructions = instruction
        if TRACE_AGENT in self.tracing:
            print(f"[TRACE_AGENT] {self._name} instruction updated:\n{instruction}")

    def getDescription(self):
        return self._description

    def getUnderlyingAgent(self):
        return self._agent

    def setHandoffAgents(self, agents: list["Agent"]):
        self._agent.handoffs = [agent.asHandoff() for agent in agents]

    def asHandoff(self):
        return handoff(self._agent)

    @staticmethod
    def _inferDescription(instruction: str, fallback: str) -> str:
        for line in instruction.splitlines():
            candidate = line.strip()
            if candidate:
                return candidate
        return fallback
