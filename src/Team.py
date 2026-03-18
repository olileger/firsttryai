from abc import ABC, abstractmethod


class Team(ABC):
    @abstractmethod
    async def run(self, task: str):
        ...
