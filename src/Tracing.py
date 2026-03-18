import argparse
from typing import Any, Iterable

from agents import Agent as OpenAIAgent
from agents.items import ModelResponse, TResponseInputItem
from agents.lifecycle import AgentHooksBase
from agents.tool import Tool

TRACE_AGENT = "agent"
TRACE_TEAM = "team"
TRACE_TOOL = "tool"
TRACE_LLM = "llm"
VALID_TRACE_LEVELS = frozenset({TRACE_AGENT, TRACE_TEAM,TRACE_TOOL, TRACE_LLM})


def parse_tracing_levels(value: str) -> frozenset[str]:
    levels = [item.strip().lower() for item in value.split(",")]
    if not levels or any(not level for level in levels):
        raise argparse.ArgumentTypeError(
            "Tracing must be a comma-separated list containing agent, tool, and/or llm."
        )

    invalid_levels = sorted({level for level in levels if level not in VALID_TRACE_LEVELS})
    if invalid_levels:
        raise argparse.ArgumentTypeError(
            "Invalid tracing level(s): "
            + ", ".join(invalid_levels)
            + ". Supported values are: agent, tool, llm."
        )

    return frozenset(levels)


def _agent_name(agent: Any) -> str:
    return getattr(agent, "name", agent.__class__.__name__)


def _tool_name(tool: Tool) -> str:
    return getattr(tool, "name", tool.__class__.__name__)


def _preview(value: Any) -> str:
    return str(value)


def _preview_turn_input(input_items: list[TResponseInputItem]) -> str:
    if not input_items:
        return "<empty>"
    return _preview(input_items[-1])


class StdoutAgentHooks(AgentHooksBase[Any, OpenAIAgent[Any]]):
    def __init__(self, trace_levels: Iterable[str]):
        self._trace_levels = set(trace_levels)

    def _is_enabled(self, trace_level: str) -> bool:
        return trace_level in self._trace_levels

    async def on_start(self, context, agent: OpenAIAgent[Any]) -> None:
        if not self._is_enabled(TRACE_AGENT):
            return
        print(
            f"[agent] start: name={_agent_name(agent)} request={_preview_turn_input(context.turn_input)}",
            flush=True
        )

    async def on_end(self, context, agent: OpenAIAgent[Any], output: Any) -> None:
        if not self._is_enabled(TRACE_AGENT):
            return
        print(
            f"[agent] end: name={_agent_name(agent)} output={_preview(output)}",
            flush=True
        )

    async def on_handoff(self, context, agent: OpenAIAgent[Any], source: OpenAIAgent[Any]) -> None:
        if not self._is_enabled(TRACE_AGENT):
            return
        print(
            "[agent] handoff: "
            f"from={_agent_name(source)} to={_agent_name(agent)} "
            f"request={_preview_turn_input(context.turn_input)}",
            flush=True
        )

    async def on_tool_start(self, context, agent: OpenAIAgent[Any], tool: Tool) -> None:
        if not self._is_enabled(TRACE_TOOL):
            return
        print(
            "[tool] start: "
            f"tool={_tool_name(tool)} "
            f"tool_input={_preview(getattr(context, 'tool_input', None))}",
            flush=True
        )

    async def on_tool_end(self, context, agent: OpenAIAgent[Any], tool: Tool, result: str) -> None:
        if not self._is_enabled(TRACE_TOOL):
            return
        print(
            "[tool] end: "
            f"tool={_tool_name(tool)} "
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
        if not self._is_enabled(TRACE_LLM):
            return
        print(
            "[llm] start: "
            f"name={_agent_name(agent)} items={len(input_items)} "
            f"request={_preview_turn_input(input_items)}",
            flush=True
        )
        if system_prompt:
            print(f"[llm] system prompt: {_preview(system_prompt)}", flush=True)

    async def on_llm_end(
        self,
        context,
        agent: OpenAIAgent[Any],
        response: ModelResponse,
    ) -> None:
        if not self._is_enabled(TRACE_LLM):
            return
        print(
            "[llm] end: "
            f"name={_agent_name(agent)} "
            f"response_id={response.response_id} "
            f"request_id={response.request_id} "
            f"output_items={len(response.output)}",
            flush=True
        )


def create_stdout_agent_hooks(trace_levels: Iterable[str] | None) -> StdoutAgentHooks | None:
    if trace_levels is None:
        return None

    normalized_levels = frozenset(trace_levels)
    if not normalized_levels:
        return None

    return StdoutAgentHooks(normalized_levels)
