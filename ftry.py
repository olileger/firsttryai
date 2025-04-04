import argparse
import asyncio
from autogen_agentchat.ui import Console


async def main():
    """
    Entry point for the ftry | yai CLI.
    Note for the dumb creator of this CLI => In dev mode:
    - pip install e .       # install the package in editable mode => TODO after each change into setup.py
    - pip uninstall ftry    # remove the package from the environment
    """

    # Commands: definitions
    p = argparse.ArgumentParser(description="ftry CLI")
    subcmd = p.add_subparsers(dest="subcmd", required=True)

    # 'pop' command
    pop = subcmd.add_parser("pop", help="Pop up an agent or team")
    popgroup = pop.add_mutually_exclusive_group(required=True)
    popgroup.add_argument("-t", "--team", type=str, help="Team description file")
    popgroup.add_argument("-a", "--agent", type=str, help="Agent description file")

    # 'kickflip' command
    kickflip = subcmd.add_parser("kickflip", help="Ask for a kickflip")

    # Commands: function calling
    args = p.parse_args()
    if args.subcmd == "pop":
        if args.team:
            print("Creating team from file: ", args.team)
            from src import TeamHelper
            t = await TeamHelper.createTeam(args.team)
            task = input("Task: ")
            await Console(t.run_stream(task=task))
        elif args.agent:
            print("Creating agent from file: ", args.agent)
            from src import AgentHelper
            a = await AgentHelper.createAgent(args.agent)
            task = input("Task: ")
            await Console(a.run_stream(task=task))
    elif args.subcmd == "kickflip":
        print("Hey bro! Do a kickflip!")


if __name__ == "__main__":
    asyncio.run(main())