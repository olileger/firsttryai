# Teams Command

The `teams` command allows you to run multiple GenAI teams in parallel based on configurations provided in a YAML file.

## Usage

```bash
ftry teams <teams_config.yaml>
```

- `<teams_config.yaml>`: Path to a YAML file that describes the teams to run

## YAML Configuration Structure

The teams configuration file should follow this structure:

```yaml
teams:
  - name: TeamA                    # Optional: Team name for identification
    config: ./path/to/team.yaml    # Path to existing team configuration file
    task: "Your task description"  # Optional: Task to execute
  
  - name: TeamB                    # Optional: Team name for identification  
    model:                         # Model configuration
      name: gpt-4o-2024-08-06
      provider: openai
      api-key: env:OAI_API_KEY
    termination:                   # Termination conditions
      keyword: __END__
      max-round: 10
    agents:                        # List of agents (file references)
      - file: ./agents/agent1.yaml
      - file: ./agents/agent2.yaml
    prompt: |                      # Team coordination prompt
      Your team coordination instructions here.
    task: "Your task description"  # Optional: Task to execute
```

## Configuration Options

### Team Configuration

Each team in the `teams` list can be configured in two ways:

#### 1. External Configuration File
```yaml
- name: TeamA
  config: ./path/to/existing/team.yaml
  task: "Optional task description"
```

#### 2. Inline Configuration
```yaml
- name: TeamB
  model:
    name: gpt-4o-2024-08-06
    provider: openai
    api-key: env:OAI_API_KEY
  termination:
    keyword: __END__
    max-round: 10
  agents:
    - file: ./agents/agent1.yaml
    - file: ./agents/agent2.yaml
  prompt: "Team coordination prompt"
  task: "Optional task description"
```

### Required Fields

- `teams`: Root key containing list of team configurations
- Either `config` (external file) OR inline configuration with:
  - `model`: Model configuration
  - `agents`: List of agent file references
  - `prompt`: Team coordination prompt
  - `termination`: Termination conditions

### Optional Fields

- `name`: Team name for identification in output (defaults to "Team-N")
- `task`: Task description to execute (defaults to generic introduction)

## Features

- **Parallel Execution**: All teams run concurrently
- **Output Separation**: Clear identification of output by team name
- **Error Handling**: Individual team failures don't stop other teams
- **Summary Report**: Shows success/failure status for all teams
- **Exit Codes**: Non-zero exit code if any team fails

## Example Output

```
Loading teams configuration from: ./samples/teams.yaml

🚀 Starting TeamA...
📝 TeamA - Task: Help me improve a prompt for generating creative writing ideas.
🔄 TeamA - Starting execution...

🚀 Starting TeamB...
📝 TeamB - Task: Create a prompt for summarizing technical documentation.
🔄 TeamB - Starting execution...

[Team execution output...]

✅ TeamA - Completed successfully
✅ TeamB - Completed successfully

============================================================
TEAMS EXECUTION SUMMARY
============================================================
✅ TeamA: SUCCESS
✅ TeamB: SUCCESS

Successful teams: 2
Failed teams: 0

🎉 All teams completed successfully!
```

## Example Configuration File

See `samples/teams.yaml` for a complete example configuration.

## Limitations

- Currently only supports agent file references (not inline agent definitions)
- All teams must use compatible model providers with available API keys
- No concurrency limits or execution priorities (all teams run simultaneously)