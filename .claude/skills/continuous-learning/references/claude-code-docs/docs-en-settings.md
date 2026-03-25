# Claude Code settings

> Configure Claude Code with global and project-level settings, and environment variables.

Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the `/config` command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options.

## Configuration scopes

Claude Code uses a **scope system** to determine where configurations apply and who they're shared with. Understanding scopes helps you decide how to configure Claude Code for personal use, team collaboration, or enterprise deployment.

### Available scopes

| Scope       | Location                                                                           | Who it affects                       | Shared with team?      |
| :---------- | :--------------------------------------------------------------------------------- | :----------------------------------- | :--------------------- |
| **Managed** | Server-managed settings, plist / registry, or system-level `managed-settings.json` | All users on the machine             | Yes (deployed by IT)   |
| **User**    | `~/.claude/` directory                                                             | You, across all projects             | No                     |
| **Project** | `.claude/` in repository                                                           | All collaborators on this repository | Yes (committed to git) |
| **Local**   | `.claude/settings.local.json`                                                      | You, in this repository only         | No (gitignored)        |

### When to use each scope

**Managed scope** is for:

* Security policies that must be enforced organization-wide
* Compliance requirements that can't be overridden
* Standardized configurations deployed by IT/DevOps

**User scope** (`~/.claude/`) is for:

* Personal preferences that apply across all projects
* API keys and credentials (preferably use a secrets manager)
* Default model selections
* Theme and UI preferences

**Project scope** (`.claude/` in repository) is for:

* Team-wide configurations that should be version-controlled
* Project-specific tool settings
* Development environment standards
* Documentation and guides for collaborators

**Local scope** (`.claude/settings.local.json`) is for:

* Temporary testing or debugging
* Machine-specific overrides (e.g., different hardware)
* Sensitive settings that shouldn't be committed (automatically gitignored)

## Configuration files

Claude Code uses structured configuration files that you can edit directly or through the `/config` command. The configuration system follows a precedence order:

1. **Managed** settings (enforced by IT/organization, highest priority)
2. **User** settings (`~/.claude/settings.json`)
3. **Project** settings (`.claude/settings.json`)
4. **Local** settings (`.claude/settings.local.json`, lowest priority)

Settings from higher-priority scopes override lower-priority ones.

### settings.json file structure

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 8096,
  "thinking": {
    "enabled": false,
    "budget_tokens": 10000
  },
  "autocomplete": {
    "enabled": true,
    "mode": "instant"
  },
  "codeAssistance": {
    "enabled": true,
    "suggestions": "on_demand"
  },
  "tools": {
    "enabled": true,
    "bash": {
      "enabled": true
    }
  },
  "editor": {
    "theme": "light",
    "font_family": "Menlo",
    "font_size": 12
  },
  "terminal": {
    "enabled": true,
    "shell": "bash"
  },
  "git": {
    "auto_commit": false
  }
}
```

## Available settings

### Model settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `model` | string | `claude-3-5-sonnet-20241022` | The Claude model to use for code assistance |
| `max_tokens` | number | `8096` | Maximum tokens in response |

### Thinking settings

Extended thinking allows Claude to reason through complex code problems before responding. Configure with:

```json
{
  "thinking": {
    "enabled": true,
    "budget_tokens": 10000
  }
}
```

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `thinking.enabled` | boolean | `false` | Enable extended thinking for complex tasks |
| `thinking.budget_tokens` | number | `10000` | Maximum tokens Claude can use for thinking |

### Autocomplete settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `autocomplete.enabled` | boolean | `true` | Enable code autocomplete suggestions |
| `autocomplete.mode` | string | `instant` | `instant` or `on_demand` for when suggestions appear |

### Code assistance settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `codeAssistance.enabled` | boolean | `true` | Enable code generation and refactoring assistance |
| `codeAssistance.suggestions` | string | `on_demand` | `on_demand` for opt-in, or other modes |

### Tools settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `tools.enabled` | boolean | `true` | Enable tool use (bash, file operations, etc.) |
| `tools.bash.enabled` | boolean | `true` | Enable bash execution |

### Editor settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `editor.theme` | string | `light` | UI theme: `light` or `dark` |
| `editor.font_family` | string | `Menlo` | Font for code display |
| `editor.font_size` | number | `12` | Font size in points |

### Terminal settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `terminal.enabled` | boolean | `true` | Enable terminal interface |
| `terminal.shell` | string | `bash` | Shell to use: `bash`, `zsh`, `fish` |

### Git settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `git.auto_commit` | boolean | `false` | Automatically commit changes when requested |
| `git.gpg_sign` | boolean | `false` | Automatically sign commits with GPG |

## Environment variables

You can configure Claude Code behavior using environment variables. These are useful for CI/CD, scripting, or temporary overrides.

### Common environment variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CLAUDE_MODEL` | Override the model setting | `CLAUDE_MODEL=claude-3-opus-20250219` |
| `CLAUDE_MAX_TOKENS` | Override max tokens | `CLAUDE_MAX_TOKENS=4096` |
| `CLAUDE_API_KEY` | API key for authentication | `CLAUDE_API_KEY=sk-ant-...` |
| `CLAUDE_THINKING_ENABLED` | Enable extended thinking | `CLAUDE_THINKING_ENABLED=true` |
| `CLAUDE_THINKING_BUDGET` | Thinking token budget | `CLAUDE_THINKING_BUDGET=5000` |

### Setting environment variables

**On macOS/Linux:**

```bash
# Temporary (current shell only)
export CLAUDE_MODEL=claude-3-opus-20250219
claude

# Persistent (add to ~/.zshrc or ~/.bashrc)
echo 'export CLAUDE_MODEL=claude-3-opus-20250219' >> ~/.zshrc
```

**On Windows:**

```powershell
# Temporary (current shell only)
$env:CLAUDE_MODEL="claude-3-opus-20250219"
claude

# Persistent (set user/system environment variable via Settings)
setx CLAUDE_MODEL "claude-3-opus-20250219"
```

## Project-specific configuration

Store team configurations in `.claude/settings.json` in your repository. When Claude Code is used in that project, these settings apply to all collaborators.

### Example project configuration

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 6000,
  "codeAssistance": {
    "enabled": true,
    "suggestions": "on_demand"
  },
  "tools": {
    "bash": {
      "enabled": true
    }
  },
  "editor": {
    "theme": "dark"
  }
}
```

This ensures your team uses consistent settings for the project.

## Disabling features

### Disable autocomplete

```json
{
  "autocomplete": {
    "enabled": false
  }
}
```

### Disable tools (bash, file operations)

```json
{
  "tools": {
    "enabled": false
  }
}
```

This prevents Claude Code from executing code or modifying files.

### Disable specific tools

```json
{
  "tools": {
    "bash": {
      "enabled": false
    }
  }
}
```

## Troubleshooting

### Settings not applying

1. Check which scope your settings are in — verify precedence order
2. Restart Claude Code after changing settings
3. Verify JSON syntax in your settings file (use `/config` for visual editing)
4. Check for conflicting local settings (`.claude/settings.local.json`)

### Finding your settings files

- **User settings**: `~/.claude/settings.json`
- **Project settings**: `.claude/settings.json` (in your repository root)
- **Local settings**: `.claude/settings.local.json` (in your repository root, gitignored)

### Reverting to defaults

Delete or rename your settings file to restore defaults:

```bash
# Revert user settings
rm ~/.claude/settings.json

# Revert project settings
rm .claude/settings.json
```

Then restart Claude Code.

## Advanced configuration

### Using configuration with CI/CD

For automated workflows, use environment variables to configure Claude Code:

```bash
export CLAUDE_API_KEY=${{ secrets.CLAUDE_API_KEY }}
export CLAUDE_MODEL=claude-3-5-sonnet-20241022
export CLAUDE_MAX_TOKENS=4096
claude --help
```

### Team guidelines

Share configuration best practices with your team:

1. **Don't commit API keys** — use local settings or environment variables
2. **Document custom settings** — explain non-standard configurations in your project README
3. **Version control project settings** — keep `.claude/settings.json` in git, but gitignore `.claude/settings.local.json`
4. **Use consistent models** — agree on a default model for reproducibility

## Related resources

- [Getting started with Claude Code](https://code.claude.com/docs/getting-started)
- [CLI reference](https://code.claude.com/docs/cli)
- [Advanced features](https://code.claude.com/docs/advanced)
