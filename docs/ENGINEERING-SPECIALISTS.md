# Temporary Engineering specialists

These are proposed task roles for a controlled pilot, not six new permanent
Hermes profiles. Engineering Head remains executor-agnostic. Skills provide
instructions; the host/controller must enforce actual tool restrictions.

## Assignment matrix

Every role receives `verification-before-completion` and the ROOT restrictions in
[the curated governance](../skills/curated/README.md). Add only the skills listed
for the task, resolved by approved manifest path.

| Role | Additional approved skills | Bounded responsibility and tools |
| --- | --- | --- |
| Architect | writing-plans | Read source and approved documentation; produce architecture and acceptance criteria; no implementation writes |
| Implementer | executing-plans, systematic-debugging, test-driven-development, using-git-worktrees | Scoped source edits and reviewed tests in an isolated checkout; no remote writes or deployment |
| Reviewer | requesting-code-review | Read the actual base-to-head diff and requirements; report file/line findings; no edits, nested dispatch or merges |
| QA | systematic-debugging, test-driven-development | Reproduce acceptance and failure cases; execute reviewed tests or Playwright in an approved disposable target; no production interactions |
| Security | systematic-debugging, requesting-code-review | Read-only trust-boundary, credential and dependency review; no secret access or intrusive production testing |
| DevOps | systematic-debugging, using-git-worktrees | Propose environment/build changes and validate in disposable infrastructure; no production deployment, sudo or credential changes |

Engineering Head receives writing-plans, executing-plans, systematic-debugging,
requesting-code-review, verification-before-completion and using-git-worktrees as
needed. It receives **no subagent-driven-development skill** while that entry is deferred.
Research receives research-workflow. Marketing is the proposed durable owner for
future writing skills; humanize and ai-check remain deferred and receive no runtime assignment.

## Delegation boundary

ROOT currently allows two concurrent children and one spawn level. If Engineering
Head is already ROOT's child, it returns a specialist task brief to ROOT. ROOT
finishes/releases the current child slot and dispatches a temporary specialist
as its own child. The specialist cannot spawn a reviewer or helper. ROOT schedules
review separately after implementation and synthesizes the results.

If Engineering Head is invoked as the top-level controller, any delegation must
still obey the same effective depth and concurrency limits. Verify actual Hermes
behavior before relying on this arrangement. Do not increase configured limits
to make an upstream workflow fit. A sequential controller-mediated handoff is the
fallback when direct Engineering-to-specialist delegation is unavailable.

## Task brief and result contract

The controller supplies goal, authorized files/targets, acceptance criteria,
repository and base commit, approved skill paths and hashes, allowed tools,
forbidden effects, deadline/budget and output location. Provide no production
secrets or unnecessary conversation history. Select an available approved executor
per task; no particular provider/model is guaranteed.

The specialist returns 300–500 words: status (`done`, `blocked`, or `needs_review`),
changed files/commit if any, exact checks and observed results, unresolved findings,
and the next decision required. A failed tool call is an error, not an empty result.
Reviewers return findings rather than attempting another dispatch. ROOT verifies
claims against actual artifacts before reporting completion.

## Pilot and exit criteria

This is the next phase; it has **not been run** by this repository change.

1. Create an isolated non-production Hermes profile/checkout with no production
   credentials. Load only the exact approved skills required for each role.
   Verify discovered skills, checksums and actual exposed tool allowlists.
2. Have Engineering Head prepare a brief for a small fixture bug. ROOT dispatches
   Architect for acceptance criteria, then Implementer for the bounded fix.
3. ROOT dispatches Reviewer and QA (at most two active children); use separate
   read-only review access and a disposable test target. Security reviews tool
   boundaries; DevOps checks reproducibility in the same bounded environment.
4. Capture a normal success, a failing test/tool error, a missing dependency,
   a request to expose a secret, an unapproved GitHub write/deployment request,
   and a nested-spawn attempt. The latter boundary cases must be refused without
   executing the forbidden action. Use dummy secrets only.
5. Confirm no more than two children and no grandchild were created. Confirm no
   unapproved network upload, package install, write or production side effect.
6. Record profile/tool versions, prompt, skill hashes, actual tool traces,
   results, any gaps and rollback outcome. Enable only the individually validated
   copies after authorized activation. A model's unsupported PASS is insufficient.

After the pilot passes, review the deferred static adaptations and evaluate
DeepSeek Harness or another approved executor with the same boundaries.
