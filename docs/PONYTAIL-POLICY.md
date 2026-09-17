# Ponytail Engineering Policy

## Purpose

Ponytail is ROOT Engineering's simplicity discipline.

Its goal is not minimum lines of code at any cost. Its goal is to avoid
unnecessary engineering while preserving correctness, security, clarity,
validation, and maintainability.

## Current rollout

Ponytail is enabled for:

- Engineering

Ponytail is not enabled for:

- Chief
- Research
- Marketing
- Operations

Do not enable it globally without separate validation.

## Decision ladder

For coding and architecture tasks, Engineering should consider solutions in this
order:

1. Does new code need to exist at all?
2. Can existing project code already solve the problem?
3. Can the language standard library solve it?
4. Can a native platform capability solve it?
5. Can an already-installed dependency solve it?
6. Can the requirement be satisfied with a small, clear implementation?
7. Add new abstractions or dependencies only when the requirement justifies them.

## Priorities

Prefer:

- existing code
- standard library
- native platform features
- existing dependencies
- explicit small functions
- simple control flow
- direct solutions

Avoid by default:

- speculative abstractions
- unnecessary wrapper classes
- unnecessary helper layers
- new dependencies for trivial functionality
- premature extensibility
- generic frameworks for narrow requirements
- clever one-liners that reduce readability

## Safety boundary

Simplicity does not override:

- correctness
- security
- input validation
- authorization
- error handling
- data integrity
- maintainability
- accessibility
- production safeguards

If the shorter implementation is less safe or less clear, choose the safer and
clearer implementation.

## Example

For checking whether a Python list is empty, prefer:

```python
if not items:
    ...
```

If a reusable helper is explicitly required:

```python
def is_empty(items: list) -> bool:
    return not items
```

Do not introduce a utility class, dependency, service, or generic collection
abstraction without an actual requirement.

## Integration

ROOT does not install the full upstream Ponytail Hermes plugin.

The upstream plugin was blocked by Hermes' security scanner because the
repository contains benchmark, test, CI, and other executable or security-test
content that triggered the scanner.

ROOT keeps the scanner enabled.

Engineering instead uses the vetted Ponytail instruction skill located under:

```text
$HERMES_HOME/skills/ponytail/
```

Engineering's persistent instructions load the Ponytail discipline for coding
and architecture tasks.

## Validation

The integration is considered working when a fresh Engineering session,
without explicitly requesting Ponytail, loads the `ponytail` skill during a
coding-design task.

Initial validation asked Engineering how to implement a reusable Python
emptiness check.

Engineering:

- loaded Ponytail automatically
- preferred Python truthiness
- used no dependency
- avoided unnecessary abstraction
- proposed a minimal implementation

## Relationship to other token-efficiency layers

ROOT currently uses:

- Headroom: reduce model/context payload
- RTK: reduce terminal/tool output
- Serena: reduce unnecessary code retrieval
- Ponytail: reduce unnecessary code and engineering complexity

These solve different problems and are complementary.

## Caveman comparison

ROOT evaluated the Caveman skill against Ponytail.

Caveman primarily compresses agent prose and communication style.

Ponytail primarily reduces unnecessary implementation complexity while already
limiting unrequested explanatory prose.

ROOT does not install Caveman as a separate Engineering skill because the
overlap does not justify another always-on instruction layer.

ROOT retains one useful Caveman principle: routine Engineering communication
should be concise, while security, destructive actions, production changes,
approval boundaries, and ambiguity-sensitive procedures must remain explicit.
