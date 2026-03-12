import re
from typing import List
from agents import Agent as OpenAIAgent, Runner
from src.Agent import Agent
from src.Model import Model


class Team:
    """A manager agent that delegates to participant agents as native SDK tools."""

    def __init__(self, name: str, agents: List[Agent], model: Model, manager_prompt: str, max_turns: int):
        
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

        print(f"Manager prompt: {self._buildManagerInstructions(manager_prompt)}")

        self._manager = OpenAIAgent(
            name=name,
            instructions=self._buildManagerInstructions(manager_prompt),
            tools=self._buildParticipantTools(),
            model=model.getUnderlyingModel()
        )

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
            "<Speaker Selection>"
            "Delegate work by calling the relevant tools when specialized expertise is needed.\n"
            f"Available Tools: {self.participants}\n"
            f"Tools descriptions:\n{self.roles}\n\n"
            "</Speaker Selection>"
        )
    
    def _buildParticipantTools(self):
        tools = []
        for agent in self.agents:
            tools.append(
                agent.getUnderlyingAgent().as_tool(
                    tool_name=agent.getName(),
                    tool_description=agent.getDescription()
                )
            )
        return tools
    
    async def run(self, task: str):
        return await Runner.run(self._manager, task, max_turns=self.max_turns)

