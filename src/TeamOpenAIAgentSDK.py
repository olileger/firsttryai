from typing import List

from src.Agent import Agent
from src.AgentOpenAIAgentSDK import AgentOpenAIAgentSDK
from src.Model import Model
from src.Team import Team
from src.Tracing import TRACE_TEAM


class TeamOpenAIAgentSDK(Team):
    """OpenAI Agent SDK implementation of the Team interface."""

    def __init__(
        self,
        name: str,
        agents: List[Agent],
        model: Model,
        manager_prompt: str,
        max_turns: int,
        tracing: frozenset[str] | None = None
    ):
        if not agents:
            raise ValueError("A team must contain at least one agent.")
        if max_turns < 1:
            raise ValueError("A team must allow at least one turn.")

        participant_names = [agent.getName() for agent in agents]
        if len(set(participant_names)) != len(participant_names):
            raise ValueError("Each agent in a team must have a unique name.")

        self.name = name
        self.agents = agents
        self.max_turns = max_turns
        self.tracing = frozenset() if tracing is None else tracing

        manager_instructions = self._buildManagerInstructions(manager_prompt)
        if TRACE_TEAM in self.tracing:
            print(f"Manager prompt:\n{manager_instructions}")

        self._manager = AgentOpenAIAgentSDK(
            name=name,
            instruction=manager_instructions,
            model=model,
            description=name,
            tools=self._buildParticipantTools(),
            tracing=tracing
        )

    def _buildParticipants(self):
        return ", ".join(agent.getName() for agent in self.agents)

    def _buildRoles(self):
        return "\n".join(
            f"\t- {agent.getName()}: {agent.getDescription()}"
            for agent in self.agents
        )

    def _buildManagerInstructions(self, manager_prompt: str) -> str:
        self.participants = self._buildParticipants()
        self.roles = self._buildRoles()
        return (
            f"{manager_prompt}\n".replace("{participants}", self.participants).replace("{roles}", self.roles) +
            "<Speaker Selection>\n"
            "Delegate work by calling the relevant tools when specialized expertise is needed.\n"
            f"Available Tools: {self.participants}\n"
            f"Tools descriptions:\n{self.roles}\n\n"
            "</Speaker Selection>"
        )

    def _buildParticipantTools(self):
        return [agent.asTool() for agent in self.agents]

    async def run(self, task: str):
        return await self._manager.run(task, max_turns=self.max_turns)
