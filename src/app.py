import asyncio
import nest_asyncio
nest_asyncio.apply()

from ag_AgentChat_AgentsExt import AgentHelper
from ag_AgentChat_TeamsExt import TeamHelper
from autogen_agentchat.ui import Console


async def main():
    pr = await AgentHelper.CreateAgent("Prompter", './samples/pr.txt', 'OAI_API_KEY')
    re = await AgentHelper.CreateAgent("Reviewer", './samples/re.txt', 'OAI_API_KEY')
    ru = await AgentHelper.CreateAgent("Runner", './samples/ru.txt', 'OAI_API_KEY')

    t = TeamHelper.CreateTeam([pr, re, ru], './samples/team.txt', 'OAI_API_KEY')

    await Console(t.run_stream(task=
    """
    Analyse l'état du marché de la GenAI et les opportunités business qui en découlent.
    Tu proposes ta réponse sous la forme d'une liste de 5 points de 3 phrases par point.
    """))

asyncio.run(main())

# TODO
# passer les prompts au format YAML
# voir comment faire une CLI sur base python