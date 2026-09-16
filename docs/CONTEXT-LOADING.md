# ROOT Context Loading Policy

## Principle

Load the minimum context required for the current task.

## Prefer

1. current request
2. owning portfolio manifest
3. relevant department instructions
4. task-specific skill

## Do Not Automatically Load

- historical phase documents
- unrelated TEAM.md files
- unrelated department SOULs
- all skills
- full repository documentation

## Headroom

Automatic proxy compression is enabled.

Compressed context may be retrieved when exact detail is required.

Do not manually invoke Headroom for small or already-concise context.

## Goal

Prefer retrieval over persistent context.
