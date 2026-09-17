# Serena Code-Navigation Policy

## Purpose

Serena provides semantic, symbol-aware code navigation for ROOT Engineering.

It reduces unnecessary file reading by allowing Engineering to retrieve only the
symbols, references, declarations, implementations, and diagnostics required for
a task.

Serena complements the existing token-efficiency layers:

- Headroom reduces model/context payload.
- RTK reduces terminal-command output.
- Serena reduces unnecessary code retrieval and navigation.

## Current rollout

Serena is enabled for:

- Engineering

Serena is not enabled for:

- Chief
- Research
- Marketing
- Operations

Do not enable Serena globally without validation.

## Preferred usage

Engineering should prefer Serena when working with source code and the task can
be answered using semantic code structure.

Prefer:

- `get_symbols_overview`
- `find_symbol`
- `find_referencing_symbols`
- `find_declaration`
- `find_implementations`
- `get_diagnostics_for_file`

Use these before reading entire files when possible.

## When direct file reading is appropriate

Direct file reads remain appropriate when:

- reviewing configuration files
- reading documentation
- examining non-code text
- symbol lookup is insufficient
- exact surrounding context is required
- generated files or unsupported languages are involved
- Serena/LSP cannot resolve the target correctly

Avoid reading entire source files merely to locate one function or class.

## Serena vs RTK

Use Serena for semantic code understanding.

Examples:

- Where is this function defined?
- Which symbols reference this function?
- What implements this interface?
- What symbols exist in this module?
- What diagnostics affect this file?

Use RTK for shell-oriented inspection.

Examples:

- git status
- git diff
- git log
- docker ps
- tests
- lint
- find/tree/ls
- package listings

Serena and RTK are complementary rather than interchangeable.

## Write operations

Serena exposes write-capable tools including:

- replace_content
- replace_in_files
- replace_symbol_body
- insert_after_symbol
- insert_before_symbol
- rename_symbol
- safe_delete_symbol

These tools must follow ROOT's existing change-control rules.

Do not use destructive or broad refactoring operations without understanding the
impact.

Production deployment, git push, destructive changes, and other governed actions
still require the appropriate ROOT approval policy.

## MCP configuration

Engineering launches Serena as a profile-local stdio MCP server.

Project:

```text
/home/maqsood/root/root-ai
```

Context:

```text
ide
```

The Serena web dashboard is disabled.

No persistent Serena daemon is required; Hermes launches the MCP process when an
Engineering session needs it.

## Validation

A successful integration should show Serena MCP activity in:

```text
$HERMES_HOME/logs/mcp-stderr.log
```

Expected operations include:

```text
FindSymbolTool
FindReferencingSymbolsTool
GetSymbolsOverviewTool
```

Initial validation used:

```text
integrations/n8n/leantime_rpc.py
```

and symbol:

```text
is_object
```

Serena successfully:

- located the function definition
- returned its function body
- identified five references
- returned top-level symbols for the module

## Token-efficiency policy

For code exploration:

1. Start with symbol overview or symbol search.
2. Retrieve the specific symbol body needed.
3. Retrieve references only when relevant.
4. Read larger file sections only when semantic retrieval is insufficient.
5. Avoid broad recursive file reading unless required.

The goal is not maximum compression. The goal is retrieving the minimum amount
of accurate context required to complete the task.

## Change-control rules

Before changing Serena integration:

1. Work on a feature branch.
2. Run `serena project health-check`.
3. Verify MCP connectivity.
4. Test semantic retrieval on a known symbol.
5. Verify the dashboard remains disabled.
6. Validate write-capable tools separately before broad use.
7. Do not expand Serena to other profiles without a clear use case.
