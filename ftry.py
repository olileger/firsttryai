import argparse
import asyncio
from autogen_agentchat.ui import Console


#
# runTask
#
# This function runs the task using the Console UI.
# Either for Team or Agent.
#
async def runTask(args, o):
    if args.prompt:
        task = args.prompt
        print("Task passed along: ", task)
    else:
        task = input("Task: ")
    await Console(o.run_stream(task=task))


#
# runPop
#
# This function runs the pop command.
#
async def runPop(args):
    if args.team:
        print("Creating team from file: ", args.team)
        from src import TeamHelper
        t = await TeamHelper.createTeam(args.team)
        await runTask(args, t)
    elif args.agent:
        print("Creating agent from file: ", args.agent)
        from src import AgentHelper
        a = await AgentHelper.createAgent(args.agent)
        await runTask(args, a)


#
# runBuild
#
# This function runs the build command.
# It builds an agent YAML configuration from a prompt description using an LLM.
#
async def runBuild(args):
    if args.prompt:
        prompt = args.prompt
    else:
        prompt = input("Describe the agent you want to build: ")
    print(f"Building agent from prompt: {prompt}")
    from src import BuildHelper
    output_file = await BuildHelper.buildAgent(
        prompt=prompt,
        output_file=args.output,
        model_name=args.model,
        provider=args.provider,
        api_key=args.api_key,
        agent_name=args.name,
    )
    print(f"Agent built and saved to: {output_file}")


#
# runFall
#
# This function runs the fall command.
# It kills a running agent execution.
#
def runFall(args):
    print("fall: Not implemented yet.")


#
# runBreak
#
# This function runs the break command.
# It destroys an agent.
#
def runBreak(args):
    print("break: Not implemented yet.")


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
    popgroup = pop.add_mutually_exclusive_group(required=True)
    popgroup.add_argument("-t", "--team", type=str, help="Team description file")
    popgroup.add_argument("-a", "--agent", type=str, help="Agent description file")

    # 'build' command
    build = subcmd.add_parser("build", help="Build an agent from a prompt")
    build.add_argument("-p", "--prompt", type=str, help="Description of the agent to build")
    build.add_argument("-o", "--output", type=str, required=True, help="Output YAML file path")
    build.add_argument("-n", "--name", type=str, default=None, help="Agent name (generated if not provided)")
    build.add_argument("--model", type=str, required=True, help="Model name (e.g. gpt-4o)")
    build.add_argument("--provider", type=str, required=True, help="Model provider (e.g. openai, azure-openai)")
    build.add_argument("-k", "--api-key", dest="api_key", type=str, required=True, help="API key or env reference (e.g. env:OAI_API_KEY)")

    # 'fall' command
    fall = subcmd.add_parser("fall", help="Kill a running agent execution")
    fall.add_argument("-a", "--agent", type=str, required=True, help="Agent name or ID to kill")

    # 'break' command
    brk = subcmd.add_parser("break", help="Destroy an agent")
    brk.add_argument("-a", "--agent", type=str, required=True, help="Agent name or file to destroy")

    # 'kickflip' command
    subcmd.add_parser("kickflip", help="Ask for a kickflip")

    # Commands: function calling
    args = p.parse_args()
    if args.subcmd == "pop":
        await runPop(args)
    elif args.subcmd == "build":
        await runBuild(args)
    elif args.subcmd == "fall":
        runFall(args)
    elif args.subcmd == "break":
        runBreak(args)
    elif args.subcmd == "kickflip":
        runKickflip()


#
# main_sync
#
# This function is a wrapper for the main function to run it synchronously
# either from the command line or from another script.
#
def main_sync():
    asyncio.run(main())


# Entry point for the script.
if __name__ == "__main__":
    main_sync()