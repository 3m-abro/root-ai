---
name: root-orchestration
description: Integrating Claude Code into ROOT as a worker delegation target — mode selection, security mapping, phased rollout.
---
# Claude Code → ROOT Orchestration

How to integrate Claude Code into the ROOT orchestration layer as a worker delegation target.

## Integration Pattern

Claude Code is a **ROOT worker profile**, not a sidecar or fine-grained tool wrapper. ROOT dispatches a coding task to a Claude Code worker, which internally uses the existing `claude-code` skill. This mirrors how Codex and OpenCode already work.

### Default: Print Mode (`-p`) with JSON Output

Print mode is the primary integration path. It is non-interactive, exits when done, returns structured JSON, and requires no PTY or tmux overhead.

**Default invocation:**

```
claude -p '<task>' --output-format json --max-turns 10 --allowedTools 'Read,Edit,Bash' --bare
```

**Key flags:**

| Flag | Purpose |
|------|--------|
| `--output-format json` | Single result object — parse `subtype`, `result`, `session_id`, `total_cost_usd`, `num_turns` |
| `--output-format stream-json` | NDJSON for live progress streaming |
| `--max-turns N` | Cap agentic loops (print mode only) |
| `--max-budget-usd N` | Cap API spend (print mode only; minimum ~$0.05) |
| `--allowedTools 'Read,Edit,Bash'` | Restrict to needed tools only |
| `--bare` | Skip hooks/plugins/MCP/CLAUDE.md/OAuth — fastest startup, needs `ANTHROPIC_API_KEY` |
| `--model <alias>` | `sonnet`, `opus`, `haiku`, or full name |
| `--effort <level>` | `low`/`medium`/`high`/`xhigh`/`max` |
| `--fallback-model haiku` | Auto-fallback on model overload (print mode only) |

**Parsing the JSON result:**

- `subtype`: `success` / `error_max_turns` / `error_budget` — use for outcome detection
- `result`: the text output
- `session_id`: for resumption via `--resume`
- `total_cost_usd`: for cost tracking across sessions
- `num_turns`: agentic loop count

### Secondary: Interactive PTY via tmux

Only escalate to tmux when the task requires multi-turn back-and-forth or slash commands.

```
# Start
tmux new-session -d -s <name> -x 140 -y 40
tmux send-keys -t <name> 'cd /path/to/project && claude' Enter

# Handle workspace trust dialog (first visit to directory)
sleep 4 && tmux send-keys -t <name> Enter

# Send task
sleep 2 && tmux send-keys -t <name> '<task>' Enter

# Monitor — look for `❯` at bottom = waiting for input
sleep 15 && tmux capture-pane -t <name> -p -S -50

# Cleanup
tmux kill-session -t <name>
```

**Dialog handling:**

- **Workspace trust** (first visit per directory): `Enter` — default "Yes, I trust this folder" is correct
- **Permissions bypass** (only with `--dangerously-skip-permissions`): `Down` then `Enter` — default is "No, exit" which is wrong
- Trust dialog is cached per directory; permissions dialog recurs each time

### Not Primary: Worktrees and MCP

- **Worktrees** (`-w`): convenience for isolated parallel work within either print or tmux mode
- **MCP**: how Claude Code reaches external tools (GitHub, DB), not how ROOT reaches Claude Code
