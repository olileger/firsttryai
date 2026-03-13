from typing import Any

from agents import Agent as OpenAIAgent
from agents.items import ModelResponse, TResponseInputItem
from agents.lifecycle import AgentHooksBase
from agents.tool import Tool


def _agent_name(agent: Any) -> str:
    return getattr(agent, "name", agent.__class__.__name__)


def _tool_name(tool: Tool) -> str:
    return getattr(tool, "name", tool.__class__.__name__)


def _preview(value: Any, limit: int = 200) -> str:
    text = str(value).replace("\n", "\\n")
    if len(text) <= limit:
        return text
    return f"{text[:limit - 3]}..."


def _preview_turn_input(input_items: list[TResponseInputItem]) -> str:
    if not input_items:
        return "<empty>"
    return _preview(input_items[-1])


class StdoutAgentHooks(AgentHooksBase[Any, OpenAIAgent[Any]]):
    async def on_start(self, context, agent: OpenAIAgent[Any]) -> None:
        print(
            f"[agent] start: name={_agent_name(agent)} request={_preview_turn_input(context.turn_input)}",
            flush=True
        )

    async def on_end(self, context, agent: OpenAIAgent[Any], output: Any) -> None:
        print(
            f"[agent] end: name={_agent_name(agent)} output={_preview(output)}",
            flush=True
        )

    async def on_handoff(self, context, agent: OpenAIAgent[Any], source: OpenAIAgent[Any]) -> None:
        print(
            "[agent] handoff: "
            f"from={_agent_name(source)} to={_agent_name(agent)} "
            f"request={_preview_turn_input(context.turn_input)}",
            flush=True
        )

    async def on_tool_start(self, context, agent: OpenAIAgent[Any], tool: Tool) -> None:
        print(
            "[agent] tool start: "
            f"name={_agent_name(agent)} tool={_tool_name(tool)} "
            f"tool_input={_preview(getattr(context, 'tool_input', None))}",
            flush=True
        )

    async def on_tool_end(self, context, agent: OpenAIAgent[Any], tool: Tool, result: str) -> None:
        print(
            "[agent] tool end: "
            f"name={_agent_name(agent)} tool={_tool_name(tool)} "
            f"result={_preview(result)}",
            flush=True
        )

    async def on_llm_start(
        self,
        context,
        agent: OpenAIAgent[Any],
        system_prompt: str | None,
        input_items: list[TResponseInputItem],
    ) -> None:
        print(
            "[agent] llm start: "
            f"name={_agent_name(agent)} items={len(input_items)} "
            f"request={_preview_turn_input(input_items)}",
            flush=True
        )
        if system_prompt:
            print(f"[agent] llm system prompt: {_preview(system_prompt)}", flush=True)

    async def on_llm_end(
        self,
        context,
        agent: OpenAIAgent[Any],
        response: ModelResponse,
    ) -> None:
        print(
            "[agent] llm end: "
            f"name={_agent_name(agent)} "
            f"response_id={response.response_id} "
            f"request_id={response.request_id} "
            f"output_items={len(response.output)}",
            flush=True
        )
