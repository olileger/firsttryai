# First Tr(y | ai)
Pronounced "First Try", the most targeted result when you're trying skateboarding trick.
First Tr(y | ai) aims to ease building and deploying GenAI agents and teams.

## CLI Commands

### shout
Display a custom message with a megaphone emoji.

**Usage:**
```bash
# With positional argument
ftry shout "Hello World!"

# With -m flag
ftry shout -m "Hello World!"

# Interactive mode (prompts for message) - RECOMMENDED for sensitive data
ftry shout
```

**Output example:**
```bash
$ ftry shout "Hello World!"
📢 Hello World!
```

**Security Note:**
⚠️ Messages passed as command-line arguments (positional or with `-m` flag) will be visible in:
- Shell history files (`.bash_history`, `.zsh_history`, etc.)
- Process listings (`ps`, `top` commands)
- System audit logs

**For sensitive messages, use interactive mode** (run `ftry shout` without arguments) to avoid storing the message in shell history.

**Help:**
```bash
ftry shout --help
```
