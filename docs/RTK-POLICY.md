# RTK Token-Efficiency Policy

## Purpose

RTK reduces token usage by compacting noisy shell-command output before it reaches Hermes agents.

RTK complements Headroom:

- Headroom reduces prompt/context payload.
- RTK reduces terminal/tool output.
- Serena will later reduce unnecessary code reading and navigation.

## Current rollout

RTK is enabled for:

- Chief
- Engineering

RTK is not yet enabled for:

- Research
- Marketing
- Operations

Do not install the global RTK shell hook with:

```bash
rtk init -g
```

ROOT uses profile-local Hermes integration instead.

## Default RTK usage

RTK should normally rewrite routine, high-volume terminal commands such as:

- git status
- git diff
- git log
- find
- tree
- ls
- grep / rg
- docker ps
- normal test output
- lint output
- dependency/package listings

## When raw output is required

Do not rely on compressed RTK output when exact evidence matters, including:

- full stack traces
- failing-test diagnostics
- security investigations
- incident response
- exact logs
- protocol/debug traces
- benchmark evidence
- serialization or binary diagnostics
- output where truncation, grouping, or deduplication may hide the cause

In those situations, explicitly bypass RTK and inspect the original command output.

## Hermes integration

RTK is installed as a profile-local Hermes plugin:

```text
$HERMES_HOME/plugins/rtk-rewrite
```

The plugin hooks `pre_tool_call` for the Hermes `terminal` tool.

For supported commands, the plugin calls:

```text
rtk rewrite <command>
```

and returns a Hermes modification directive:

```python
{
    "action": "modify",
    "args": {
        "command": rewritten,
    },
}
```

Hermes then dispatches the rewritten command.

## Compatibility note

RTK 0.49.0's generated Hermes adapter originally mutated the incoming `args`
dictionary in-place. The Hermes version currently used by ROOT expects a
`{"action": "modify", "args": ...}` directive.

ROOT therefore uses a local compatibility patch in the Chief and Engineering
profile copies of the RTK plugin.

Do not overwrite these profile-local copies without validating the upstream
adapter against the installed Hermes hook contract.

## Validation

Check RTK savings with:

```bash
rtk gain --history
```

A successful automatic Hermes integration should show new commands such as:

```text
rtk git status
rtk git log ...
rtk docker ps
rtk find ...
```

even when the agent itself invoked the terminal normally without explicitly
requesting RTK.

## Current benchmark

Initial manual RTK benchmark:

- total savings: 32.8%
- docker ps: 67.8%
- git status: 26.3%
- find: 11.7%

After Hermes automatic rewriting was enabled for Chief:

- total commands observed: 12
- input tokens: ~4.5K
- output tokens: ~2.1K
- estimated tokens saved: ~2.4K
- overall savings: 53.2%

These figures are diagnostic measurements, not guaranteed future savings.

## Change-control rules

Before changing RTK integration:

1. Work on a feature branch.
2. Keep the current plugin copy reversible.
3. Test `rtk rewrite` independently.
4. Test the Hermes adapter independently.
5. Verify Hermes plugin discovery.
6. Run a controlled agent terminal test.
7. Check `rtk gain --history`.
8. Do not deploy RTK globally unless explicitly approved.
