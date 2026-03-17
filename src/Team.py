from typing import List
from src.Agent import Agent
from src.Model import Model
from src.Tracing import TRACE_TEAM


class Team:
    """A manager agent that delegates to participant agents through the Agent wrapper."""

    def __init__(
        self,
        name: str,
        agents: List[Agent],
        model: Model,
        manager_prompt: str,
        max_turns: int,
        tracing: frozenset[str] | None = None
    ):
        
        """ Check the input parameters for validity. """
        if not agents:
            raise ValueError("A team must contain at least one agent.")
        if max_turns < 1:
            raise ValueError("A team must allow at least one turn.")
        participant_names = [agent.getName() for agent in agents]
        if len(set(participant_names)) != len(participant_names):
            raise ValueError("Each agent in a team must have a unique name.")
        
        """ Then build the team"""
        self.name = name
        self.agents = agents
        self.max_turns = max_turns
        self.tracing = frozenset() if tracing is None else tracing

        manager_instructions = self._buildManagerInstructions(manager_prompt)
        if TRACE_TEAM in self.tracing:
            print(f"Manager prompt:\n{manager_instructions}")

        self._manager = Agent(
            name=name,
            instruction=manager_instructions,
            model=model,
            description=(
                f"Manager for the {name} team. Coordinates specialists and decides who should act next."
            ),
            tracing=tracing
        )
        self._wireHandoffs()

    def _buildParticipants(self):
        return ", ".join(agent.getName() for agent in self.agents)
    
    def _buildRoles(self):
        return "\n".join(
            f"- {agent.getName()}: {agent.getDescription()}"
            for agent in self.agents
        )

    def _buildManagerInstructions(self, manager_prompt: str) -> str:
        self.participants = self._buildParticipants()
        self.roles = self._buildRoles()
        return (
            f"{manager_prompt}\n".replace("{participants}", self.participants).replace("{roles}", self.roles) +
            "<Handoffs>\n"
            "Delegate work by handing off to the relevant specialist when specialized expertise is needed.\n"
            f"Available specialists: {self.participants}\n"
            f"Specialist descriptions:\n{self.roles}\n"
            "After a specialist responds and hands control back, decide whether another specialist should speak or whether you should answer the user.\n"
            "You are the only agent responsible for selecting the next specialist.\n"
            "</Handoffs>"
        )

    def _buildWorkerInstructions(self, agent: Agent) -> str:
        return (
            f"{agent.getInstruction()}\n"
            "<Handoffs>\n"
            f"You are part of the {self.name} team and you are coordinated by the {self.name} manager.\n"
            f"When you finish your contribution, hand off control back to {self.name}.\n"
            "</Handoffs>"
        )

    def _wireHandoffs(self):
        self._manager.setHandoffAgents(self.agents)
        """for agent in self.agents:
        agent.updateInstruction(self._buildWorkerInstructions(agent))
        agent.setHandoffAgents([self._manager])"""
    
    async def run(self, task: str):
        return await self._manager.run(task, max_turns=self.max_turns)

