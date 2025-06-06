import asyncio
import os
import tempfile
from src import FileHelper
from src import TeamHelper
from autogen_agentchat.ui import Console


async def runTeamsFromConfig(configPath: str):
    """
    Runs multiple teams in parallel based on a YAML configuration file.
    
    :param configPath: Path to the teams configuration YAML file.
    """
    config = FileHelper.readYamlFile(configPath)
    
    if "teams" not in config:
        raise Exception("YAML file must contain 'teams' key")
    
    teams_config = config["teams"]
    if not isinstance(teams_config, list):
        raise Exception("'teams' must be a list")
    
    # Create tasks for each team
    tasks = []
    for i, team_config in enumerate(teams_config):
        task = asyncio.create_task(runSingleTeam(team_config, i))
        tasks.append(task)
    
    # Run all teams in parallel and collect results
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Print summary
    print("\n" + "="*60)
    print("TEAMS EXECUTION SUMMARY")
    print("="*60)
    
    failed_teams = []
    successful_teams = []
    
    for i, result in enumerate(results):
        team_name = teams_config[i].get("name", f"Team-{i+1}")
        if isinstance(result, Exception):
            print(f"❌ {team_name}: FAILED - {str(result)}")
            failed_teams.append(team_name)
        else:
            print(f"✅ {team_name}: SUCCESS")
            successful_teams.append(team_name)
    
    print(f"\nSuccessful teams: {len(successful_teams)}")
    print(f"Failed teams: {len(failed_teams)}")
    
    if failed_teams:
        print(f"\nFailed teams: {', '.join(failed_teams)}")
        exit(1)
    else:
        print("\n🎉 All teams completed successfully!")


async def runSingleTeam(team_config: dict, team_index: int):
    """
    Runs a single team based on its configuration.
    
    :param team_config: Dictionary containing team configuration.
    :param team_index: Index of the team for identification.
    """
    team_name = team_config.get("name", f"Team-{team_index+1}")
    
    print(f"\n🚀 Starting {team_name}...")
    
    try:
        # Check if team has external config file
        if "config" in team_config:
            # Use external config file
            config_path = team_config["config"]
            if not os.path.exists(config_path):
                raise Exception(f"Config file not found: {config_path}")
            team = await TeamHelper.createTeam(config_path)
        else:
            # Create temporary config file from inline configuration
            team_yaml = createTeamYamlFromConfig(team_config)
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
                temp_file.write(team_yaml)
                temp_config_path = temp_file.name
            
            try:
                team = await TeamHelper.createTeam(temp_config_path)
            finally:
                # Clean up temporary file
                os.unlink(temp_config_path)
        
        # Get task input
        task_input = team_config.get("task", "Please introduce yourselves and start working.")
        
        print(f"📝 {team_name} - Task: {task_input}")
        print(f"🔄 {team_name} - Starting execution...")
        
        # Run the team with the Console UI but capture output
        await Console(team.run_stream(task=task_input))
        
        print(f"✅ {team_name} - Completed successfully")
        
    except Exception as e:
        print(f"❌ {team_name} - Failed: {str(e)}")
        raise e


def createTeamYamlFromConfig(team_config: dict) -> str:
    """
    Creates a team YAML configuration string from the team config dictionary.
    
    :param team_config: Dictionary containing team configuration.
    :return: YAML string for team configuration.
    """
    import yaml
    
    # Create default team structure
    team_yaml = {
        "name": team_config.get("name", "Generated Team"),
        "model": team_config.get("model", {
            "name": "gpt-4o-2024-08-06",
            "provider": "openai", 
            "api-key": "env:OAI_API_KEY"
        }),
        "termination": team_config.get("termination", {
            "keyword": "__END__",
            "max-round": 10
        }),
        "agents": [],
        "prompt": team_config.get("prompt", "You are coordinating a team. Select the next team member to speak.")
    }
    
    # Process agents
    if "agents" in team_config:
        for agent_config in team_config["agents"]:
            if isinstance(agent_config, dict):
                if "file" in agent_config:
                    # Reference to external agent file
                    team_yaml["agents"].append({"file": agent_config["file"]})
                elif "agent" in agent_config:
                    # Inline agent definition - would need to create agent YAML
                    # For now, raise error as this requires more complex implementation
                    raise Exception("Inline agent definitions not yet supported. Please use 'file' references.")
            else:
                raise Exception(f"Invalid agent configuration: {agent_config}")
    
    return yaml.dump(team_yaml, default_flow_style=False)