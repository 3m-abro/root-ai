# Team Router

## Purpose

Route work to the correct portfolio team and shared department with minimal context usage.

## Routing Procedure

For every substantial task:

1. Identify the portfolio owner.
2. Identify the PRIMARY capability required.
3. Select one primary shared department.
4. Add secondary departments only when evidence shows they are needed.
5. Load only the owning team's context.
6. Delegate to the selected department head.

Do not execute work when the user asks for routing only.

## Capability Routing

### Operations

Use Operations first for:

- onboarding workflows
- business processes
- repetitive work
- operational bottlenecks
- workflow automation
- handoffs
- SOPs
- process efficiency
- delivery operations

Engineering becomes secondary if the process problem requires software changes.

### Engineering

Use Engineering first for:

- software bugs
- application performance
- architecture
- APIs
- infrastructure
- code changes
- technical integrations
- security engineering
- LLM/model infrastructure

### Marketing

Use Marketing first for:

- acquisition
- conversion
- landing-page strategy
- campaigns
- SEO
- content
- positioning
- social media

Engineering is secondary if implementation is required.

### Research

Use Research first for:

- market research
- competitor research
- technical investigation
- evaluating unknown approaches
- evidence gathering

### Finance

Use Finance first for:

- budgets
- pricing economics
- profitability
- forecasting
- financial reporting

### Legal

Use Legal first for:

- contracts
- compliance
- terms
- licensing
- regulatory questions

## Ambiguous Problems

Route according to the problem being experienced, not the artifact involved.

Example:

"Author onboarding takes too long"

Primary:
Operations

Possible secondary:
Engineering

Reason:
The stated problem is process duration. Do not assume the software is responsible.

Example:

"The author onboarding API takes 15 seconds"

Primary:
Engineering

Reason:
The stated problem is technical performance.

## Portfolio Mapping

- ReadForge-related outcome -> ReadForge
- ClearStack Studio-related outcome -> ClearStack Studio
- ROOT infrastructure/agents/FreeLLMAPI/Hermes -> ROOT Platform

## Context Efficiency

For routing-only requests:

- do not search the entire repository
- do not inspect implementation files
- do not invoke specialists
- do not load unrelated team contexts
- do not reread known organization files unless required
- prefer portfolio.yaml + team-router knowledge
- return a concise routing decision

Target response:

Owner: <team>
Primary: <department>
Secondary: <department or none>
Chain: ROOT -> Team -> Department -> temporary specialist if needed

## Efficiency Rules

- one primary department by default
- no duplicate permanent specialists
- no unrelated context
- no execution during routing-only requests
- no repository-wide search for known portfolio mappings
