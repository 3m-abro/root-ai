# Phase 5 — Worker Profiles and Delegation

## Objective

Establish ROOT's high-level worker model and validate Hermes delegation.

ROOT remains the orchestration layer.

Permanent worker profiles are intentionally broad:

- research
- engineering
- marketing
- operations

Narrow specialist tasks should use temporary Hermes child agents rather than additional permanent profiles.

## Durable Worker Profiles

### Research

Purpose:

- technical research
- market research
- competitor analysis
- evidence gathering
- synthesis

Boundaries:

- no production changes
- no publishing
- no spending
- no consequential external actions

### Engineering

Purpose:

- architecture
- coding
- debugging
- testing
- code review
- DevOps
- Git
- documentation

Boundaries:

- no git push without approval
- no production deployment without approval
- no secret exposure
- no ROOT governance changes

### Marketing

Purpose:

- positioning
- audience research
- content strategy
- campaigns
- copy
- analytics

Boundaries:

- drafting is allowed
- publishing requires approval
- paid campaigns require approval
- external outreach requires approval

### Operations

Purpose:

- workflow management
- automation
- monitoring
- reporting
- scheduling
- routine administration

Boundaries:

- prefer n8n for deterministic execution
- no irreversible actions
- no security-boundary changes
- no spending
- no external communication without approval

## Routing

ROOT routes substantial specialist work as follows:

Research:
- technical research
- market research
- competitor analysis
- evidence gathering

Engineering:
- architecture
- implementation
- debugging
- testing
- DevOps
- code review

Marketing:
- positioning
- content strategy
- campaigns
- copy
- market analysis

Operations:
- Leantime
- n8n
- monitoring
- reporting
- scheduling
- routine administration

ROOT does not delegate trivial single-tool actions.

ROOT remains responsible for:

- prioritization
- approval decisions
- cross-domain coordination
- final synthesis
- reporting to the user

## Delegation Model

Durable profiles and delegated children are different concepts.

Durable profiles:

- research
- engineering
- marketing
- operations

Temporary delegated children:

- isolated
- task-specific
- short-lived
- created with Hermes delegation
- inherit the parent tool environment
- return results to ROOT

Delegated children are not automatically one of the named durable profiles.

```text
ROOT / chief
   |
   +-- durable profiles
   |     research
   |     engineering
   |     marketing
   |     operations
   |
   +-- temporary delegate_task children
         narrow specialist tasks
         parallel research
         reviews
         isolated subtasks
```

## Delegation Discipline

Default rules:

- prefer 1-3 focused child tasks
- max nesting depth: 1
- avoid overlapping research
- request concise outputs
- target 300-500 words per child
- ROOT synthesizes final output

Phase 5 defaults:

```yaml
delegation:
  max_concurrent_children: 2
  max_spawn_depth: 1
```

Live Hermes config may differ slightly. These remain the documented Phase 5 defaults.

## Validation

Phase 5 validation confirmed:

- all four durable profiles operate independently
- each profile follows its SOUL role
- Hermes delegation works
- multiple child tasks can run in parallel
- ROOT synthesizes delegated output
- truncation can occur when child responses exceed model output limits
- output limits are mitigated through narrower task scopes and concise response requirements

## Status

Phase 5 complete.

Next:

Phase 6 — Engineering Workforce

Planned integrations:

- engineering profile
- Claude Code
- cursor-ai-dev-agents
- Git
- testing
- code review
- DevOps
- local PC execution boundary
