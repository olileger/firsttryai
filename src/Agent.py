from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    async def run(self, task: str, max_turns: int | None = None):
        ...

    @abstractmethod
    def getName(self):
        ...

    @abstractmethod
    def getInstruction(self):
        ...

    @abstractmethod
    def getDescription(self):
        ...

    @abstractmethod
    def getUnderlyingAgent(self):
        ...

    @abstractmethod
    def asTool(self):
        ...
