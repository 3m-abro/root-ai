# ROOT Context Loading Policy

## Principle

Load the minimum context required for the current task.

Prefer retrieval over persistent context.

## Normal Context Order

1. current request
2. owning portfolio manifest
3. relevant department instructions
4. task-specific skill
5. exact source material only when needed

## Do Not Automatically Load

- historical PHASE documents
- unrelated TEAM.md files
- unrelated department SOULs
- all skills
- full repository documentation
- unrelated business/project context

## Headroom Proxy

Headroom proxy compression is enabled automatically.

The model should not manually call `headroom_compress` during normal work.

## CCR References

If a tool result returns a CCR reference such as:

`<<ccr:...>>`

then:

- do not guess the missing content
- do not infer exact facts from the placeholder
- call `headroom_retrieve` only when exact source content is required
- retrieve only the specific reference needed
- avoid retrieving all compressed context proactively

## Headroom MCP Policy

Allowed:

- `headroom_retrieve` when exact compressed source content is required
- `headroom_stats` for diagnostics and benchmarks

Avoid:

- `headroom_compress` during normal requests
- unnecessary retrieval of compressed content
- retrieving CCR content when a summary is already sufficient

## Routing-Only Tasks

Normally require only:

- portfolio registry
- team-router

Do not load implementation documents.

## Engineering Tasks

Normally load:

- owning team context
- Engineering SOUL
- relevant code/document fragments
- selected skills only

Do not load unrelated portfolio or department context.

## Historical Documents

`docs/HISTORICAL/` content is loaded only when historical state is explicitly required.

## Shell-output token reduction

Routine shell output should be reduced with RTK where supported.

See:

```text
docs/RTK-POLICY.md
```
RTK reduces terminal output; Headroom reduces model/context payload. They solve different parts of the token-consumption problem and are intended to be used together.

## Semantic code retrieval

Engineering should use Serena for symbol-aware code navigation before reading
large source files.

See:

```text
docs/SERENA-POLICY.md
```
Serena reduces unnecessary code retrieval, RTK reduces shell output, and Headroom reduces model/context payload.

## Engineering simplicity discipline

Engineering applies Ponytail principles to avoid unnecessary code,
dependencies, and abstractions while preserving correctness and safety.

See:

```text
docs/PONYTAIL-POLICY.md
```
Ponytail complements Headroom, RTK, and Serena rather than replacing them.
