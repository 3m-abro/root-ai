# ADR-005 — Worker Model

## Status

Accepted

## Decision

ROOT will use four durable high-level Hermes worker profiles:

- research
- engineering
- marketing
- operations

ROOT will not create dozens of permanent specialist profiles.

Temporary specialist work will use Hermes delegated child agents.

## Rationale

A small durable worker set:

- reduces configuration sprawl
- makes routing predictable
- simplifies governance
- reduces duplicated prompts
- keeps authority boundaries clear

Temporary child agents provide specialization without creating permanent operational complexity.

Named Hermes profiles are durable worker identities. Hermes `delegate_task` children are temporary isolated subagents. They are not the same thing. Child agents inherit parent tool access and are not automatically the named research/engineering/marketing/operations profiles.

## Consequences

ROOT remains the orchestration layer.

Named profiles provide stable role identity.

Delegated children provide temporary parallel execution.

Delegated output should remain concise to reduce model truncation and synthesis overhead.
