# Curated skills review plan

This directory is a planning inventory, not an installed skills pack. All 11
entries in `manifest.json` are disabled and unreviewed. Null fields mean unknown,
not approved or permission-free. No installer or third-party skill content is included.
Names alone do not identify an upstream project. Do not assume a similarly named
local or hub skill is the intended source.

Engineering: writing-plans, executing-plans, systematic-debugging,
test-driven-development, requesting-code-review, verification-before-completion,
using-git-worktrees, subagent-driven-development.
Research: research-workflow. Writing: humanize, ai-check; decide target durable
profiles during review rather than creating a new permanent Writing worker.

## Review and integration sequence

1. Identify the upstream URL and exact skill path. Record license, immutable
   revision, and content checksum; avoid moving `latest` or branch references.
2. Review the full skill plus referenced scripts, prompts, dependencies, network
   destinations, install hooks, data access, and command execution. Fetch review
   material outside every auto-loaded runtime skill directory; do not execute it.
3. Copy `REVIEW-TEMPLATE.md` to a per-skill review record. Record requested
   permissions, risks, mitigations, compatibility with ROOT approval/delegation
   limits, reviewer, date, and explicit approval or rejection. A checksum verifies
   identity, not safety. Source changes require a new review.
4. Record an approved target profile and bounded test procedure. Validate in an
   isolated non-production profile with no production secrets and minimum tools.
   Include normal behavior, failure reporting, and refusal at permission boundaries.
5. After approval, install only the reviewed pinned copy through a separately
   authorized integration change. Record installed location, version and test
   evidence before marking enabled. Keep this manifest synchronized with reality.
6. Review the resulting diff and profile behavior. Roll back by removing the
   external-directory entry or installed copy and restoring prior profile config.

First review the planning and verification skills, then execution/debugging/testing,
then worktrees, reviews and subagent delegation. Review research and writing packs
separately. Follow with temporary Architect, Implementer, Reviewer, QA, Security,
and DevOps specifications, then an executor integration pilot.

No skill may grant GitHub writes, bypass approval, expose credentials, or raise
ROOT's delegation limits. `ai-check` output is advisory, not proof of authorship.
