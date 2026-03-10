from typing import List
from autogen_agentchat.teams import SelectorGroupChat
from src.Agent import Agent


class Team:
    """A team of Agents, each with their own skills."""

    def __init__(self, name: str, agents: List[Agent], chat: SelectorGroupChat):
        self.name = name
        self.agents = agents
        self.chat = chat
