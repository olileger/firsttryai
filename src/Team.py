from typing import List
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.Agent import Agent


class Team:
    """A team of Agents, each with their own skills."""

    def __init__(self, name: str, agents: List[Agent], model_client: OpenAIChatCompletionClient,
                 selector_prompt: str, max_round: int, termination_keyword: str):
        self.name = name
        self.agents = agents
        tc = MaxMessageTermination(max_round) | TextMentionTermination(termination_keyword)
        self.chat = SelectorGroupChat(
            participants=[a._agent for a in agents],
            model_client=model_client,
            selector_prompt=selector_prompt,
            termination_condition=tc
        )

    def run(self, task: str):
        return self.chat.run_stream(task=task)

