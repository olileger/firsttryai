import argparse
import asyncio
from agents import set_tracing_disabled
from src.Tracing import parse_tracing_levels


#
# runTask
#
# This function runs a task through either a Team or an Agent object.
#
async def runTask(args, o):
    if args.prompt:
        task = args.prompt
        print("Task passed along: ", task)
    else:
        task = input("Task: ")
    result = await o.run(task)
    print(getattr(result, "final_output", result))


#
# runPop
#
# This function runs the pop command.
#
async def runPop(args):
    if args.team:
        print("Creating team from file: ", args.team)
        from src import TeamHelper
        t = await TeamHelper.createTeam(args.team, tracing=args.tracing)
        await runTask(args, t)
    elif args.agent:
        print("Creating agent from file: ", args.agent)
        from src import AgentHelper
        a = await AgentHelper.createAgent(args.agent, tracing=args.tracing)
        await runTask(args, a)


#
# runKickflip
#
# This function runs the kickflip command.
#
def runKickflip():
    print("Hey bro! Do a kickflip!")


#
# main
#
# This function is the entry point for the ftry CLI.
#
async def main():
    # Commands: definitions
    p = argparse.ArgumentParser(description="ftry CLI")
    subcmd = p.add_subparsers(dest="subcmd", required=True)

    # 'pop' command
    pop = subcmd.add_parser("pop", help="Pop up an agent or team")
    pop.add_argument("-p", "--prompt", type=str, help="The prompt to use")
    pop.add_argument(
        "--tracing",
        type=parse_tracing_levels,
        default=frozenset(),
        help="Comma-separated tracing levels to display: agent, tool, llm"
    )
    popgroup = pop.add_mutually_exclusive_group(required=True)
    popgroup.add_argument("-t", "--team", type=str, help="Team description file")
    popgroup.add_argument("-a", "--agent", type=str, help="Agent description file")

    # 'kickflip' command
    subcmd.add_parser("kickflip", help="Ask for a kickflip")

    # Commands: function calling
    args = p.parse_args()
    if args.subcmd == "pop":
        await runPop(args)
    elif args.subcmd == "kickflip":
        runKickflip()


#
# main_sync
#
# This function is a wrapper for the main function to run it synchronously
# either from the command line or from another script.
#
def main_sync():
    set_tracing_disabled(True)
    asyncio.run(main())


# Entry point for the script.
if __name__ == "__main__":
    main_sync()
