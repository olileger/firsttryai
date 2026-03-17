# First Tr(y | ai)
Pronounced "First Try", the most targeted result when you're trying skateboarding trick.
First Tr(y | ai) aims to ease building and deploying GenAI agents and teams.

Runtime tracing can be enabled with `--tracing` on the `pop` command. Supported comma-separated levels are `agent`, `handoff`, `team`, `tool`, and `llm`. By default, tracing is disabled.

Teams are orchestrated by a manager agent that uses OpenAI Agents SDK handoffs to delegate to specialists. This preserves the running conversation for the active specialist while keeping the manager responsible for choosing who acts next.

Examples:
- `ftry pop -a .\samples\pr.yaml --tracing agent,tool`
- `ftry pop -t .\samples\team.yaml --tracing handoff`
- `ftry pop -t .\samples\team.yaml --tracing llm`
