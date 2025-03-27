import asyncio
import nest_asyncio
nest_asyncio.apply()

from ag_AgentChat_TeamsExt import TeamHelper
from autogen_agentchat.ui import Console


async def main():
    t = await TeamHelper.CreateTeam('./samples/team.yaml')

    task ="""
    Analyse l'état du marché de la GenAI et les opportunités business qui en découlent.
    Tu proposes ta réponse sous la forme d'une liste de 5 points de 3 phrases par point.
    """

    await Console(t.run_stream(task=task))

asyncio.run(main())