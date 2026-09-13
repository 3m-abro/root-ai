# Curated skills source review

Reviewed 2026-09-13 by Codex under the user request to review, vendor safe static content, commit and push. Sources were cloned into non-runtime scratch directories and no upstream code was executed. Approval covers only the exact curated files and hashes in the manifest. Eight adapted static skills are approved; three are deferred. No runtime activation or Hermes behavioral validation is claimed.

## Scope and limits

Every candidate entry file was read. For approved skills, every vendored supporting Markdown file was read. Excluded executable files and deferred supporting dependency trees are not approved or exhaustively audited. This is a source/content review, not proof of agent safety. Runtime enforcement must come from restricted tools and the controller. The manifest retains entry-file hashes for deferred candidates without copying their content. Upstream research/example claims are not independently validated.

All approved SKILL.md files receive a ROOT precedence and non-activation notice. Additional edits below remove unsafe instructions or unavailable dependencies. Supporting Markdown examples remain illustrations, not commands to execute verbatim. Upstream attribution and license metadata are retained.

## writing-plans

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md); MIT.
- Assignment: engineering, Architect.
- Tool/execution risk: low; content: instruction-only.
- Finding and disposition: Planning and local document writes. Upstream handoff references the deferred subagent skill; ROOT replaces that handoff with bounded inline execution. No dependency auto-install.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## executing-plans

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/executing-plans/SKILL.md); MIT.
- Assignment: engineering, Implementer.
- Tool/execution risk: medium; content: instruction-only.
- Finding and disposition: Local edits, tests and commits can execute project code. Replaced automatic subagent selection and unvendored finishing-a-development-branch dependency with ROOT review and approval gates.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## systematic-debugging

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/systematic-debugging/SKILL.md); MIT.
- Assignment: engineering, Implementer, QA, Security, DevOps.
- Tool/execution risk: high; content: instruction-only.
- Finding and disposition: Upstream diagnostic example prints environment values and queries keychain identities. Removed that example; only redacted presence checks are allowed. Excluded find-polluter.sh and the TypeScript helper. Supporting tracing text no longer calls them.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## test-driven-development

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/SKILL.md); MIT.
- Assignment: Implementer, QA.
- Tool/execution risk: medium; content: instruction-only.
- Finding and disposition: Test commands execute project code. Upstream unconditional delete-and-rewrite instructions are replaced with preservation of existing work and a reversible, task-scoped red-green cycle.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## requesting-code-review

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/requesting-code-review/SKILL.md); MIT.
- Assignment: engineering, Reviewer, Security.
- Tool/execution risk: medium; content: instruction-only.
- Finding and disposition: Read-only review prompt included. ROOT supplies the actual task base commit, never assumes HEAD~1 covers all changes. Only the authorized controller dispatches reviewers; a depth-limited child returns the request to ROOT.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## verification-before-completion

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/verification-before-completion/SKILL.md); MIT.
- Assignment: engineering, Architect, Implementer, Reviewer, QA, Security, DevOps.
- Tool/execution risk: low; content: instruction-only.
- Finding and disposition: Requires fresh evidence and honest failure reporting. Verification commands still need task-specific scope; this skill grants no execution or external-write authority.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## using-git-worktrees

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-git-worktrees/SKILL.md); MIT.
- Assignment: engineering, Implementer, DevOps.
- Tool/execution risk: medium; content: instruction-only.
- Finding and disposition: Worktree creation and dependency setup have filesystem and code-execution effects. Removed automatic package installation and implicit .gitignore commit. Inspect project manifests and approve concrete setup commands first.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## subagent-driven-development

- Decision: **deferred**.
- Source: [pinned entry](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md); MIT.
- Assignment: engineering.
- Tool/execution risk: high; content: executable-dependent.
- Finding and disposition: Deferred: current SKILL.md requires scripts/sdd-workspace, task-brief and review-package, plus additional prompts and finishing-a-development-branch. It also directs workspace deletion and extensive automatic delegation. Entry file reviewed; script dependency closure is not approved. Needs a separate static adaptation and depth-safe runtime pilot.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## research-workflow

- Decision: **approved_static_adaptation**.
- Source: [pinned entry](https://github.com/jwynia/agent-skills/blob/e02ec7e226a6e4f8419fd3b88a1d8e472d421b32/skills/general/research/methodology/research-workflow/SKILL.md); MIT.
- Assignment: research.
- Tool/execution risk: medium; content: instruction-only.
- Finding and disposition: Static methodology, three templates and two references reviewed. web-search CLI examples are illustrative: use an existing approved read-only search tool, never install a similarly named CLI. Example dates, claims and citations are illustrative, not verified evidence. MIT declared in skill frontmatter; no repository-wide license file found.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## humanize

- Decision: **deferred**.
- Source: [pinned entry](https://github.com/harshaneel/humanize/blob/4ec797314537ec9c2105f276d4561d240a0390ba/humanize/SKILL.md); MIT.
- Assignment: marketing.
- Tool/execution risk: high; content: instruction-only.
- Finding and disposition: Deferred: optional detector/model scoring may disclose drafts to GPTZero, Pangram or another model; detection-avoidance emphasis and plausible-specificity first-person frames need a truth-preserving, local-only adaptation. No external scoring or writing-sample upload approved. Research bibliography claims not independently verified.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.

## ai-check

- Decision: **deferred**.
- Source: [pinned entry](https://github.com/harshaneel/humanize/blob/4ec797314537ec9c2105f276d4561d240a0390ba/ai-check/SKILL.md); MIT.
- Assignment: marketing.
- Tool/execution risk: high; content: instruction-only.
- Finding and disposition: Deferred: fixed 0-27 style thresholds produce Human/AI verdicts and AI-edited fractions without local calibration. Advisory style feedback could be adapted later; current authorship classification is not approved. No detector accuracy claims verified.
- Reviewed content inventory: see this entry's `files` in the manifest.
- Validation: static integrity/structure only; runtime test pending.
