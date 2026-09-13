# Phase 6 — MCP complete; curated skills next

Status recorded: 2026-09-13. Source: the user's “ROOT Aufbauanleitung” conversation
`01368779-0354-832f-bcbd-255f7bbf3a4e`. These are reported runtime results, not a fresh
VPS test or a claim that this Git checkout deploys the live configuration.

## Completed MCP phase

| Capability | Recorded status | Evidence / limit |
| --- | --- | --- |
| Context7 | Working | Prior conversation records completion; raw test output not archived here |
| GitHub MCP | Connected, read-only | Read-only boundary reported; earlier malformed/ambiguous reads require careful interpretation |
| Playwright MCP | Validated end-to-end | TodoMVC add-and-verify test returned `PASS — ROOT Playwright MCP test 3` |
| Engineering routing | `auto:tools` | Restarted Engineering banner shows `custom:freellmapi`, `auto:tools` |

Playwright test: open `https://demo.playwright.dev/todomvc/`, add
`ROOT Playwright MCP test 3`, verify visibility, and return the PASS line only on
success. The reported run used Playwright MCP only. Repeat in the Engineering
Hermes profile after runtime changes; record tool output and verification, not
just a model's unsupported PASS assertion.

## Architecture decisions

- Hermes owns native MCP connections; no extra gateway is required for this phase.
- FreeLLMAPI routing is separate from MCP permissions and coding executor selection.
- Engineering Head uses `auto:tools`; `auto:coding` is for coding-focused execution.
- Diversify actual provider capacity pools. Two models from one provider do not
  establish independent quotas. Treat 429s as routing pressure, not MCP failure.
- The user's Google account returned a 404 for `gemini-2.5-flash`; exclude it from
  this deployment's routes. This is account evidence, not a universal retirement claim.
- Proposed replacement model names/order are not a verified inventory. Check live
  availability, tool support, quota and prompt limits before changing route chains.
- GitHub MCP stays read-only. Keep `GITHUB_READ_ONLY=1` and a narrow read allowlist
  such as `get_file_contents,list_branches,list_commits,search_code,pull_request_read,issue_read`.
  Verify the installed server's supported tools. An API error alone does not prove
  that a write boundary works; inspect exposed tools and use a refusal check.
- Do not put keys in Git. Keep provider/MCP credentials in protected runtime secrets.

Engineering MCP completion does not confirm rollout to other profiles. Context7
on Research and GitHub read-only on Chief remain deployment verification items.
The Git-owned [Engineering SOUL](../prompts/engineering/SOUL.md) must be reviewed
and synchronized with the live profile separately; this update does not deploy it.

## Next phase and exit criteria

Review the [curated manifest](../skills/curated/manifest.json) using its
[review workflow](../skills/curated/README.md). No third-party skill is installed.
Choose exact sources, pin revisions, inspect content and dependencies, assess
licenses and permissions, record approval, then validate one skill at a time in
an isolated profile. Only approved copies may enter a runtime skill directory.

After that, define temporary specialists and evaluate DeepSeek Harness or another
approved executor. End-to-end executor integration, specialist tool isolation,
and production use remain pending. Existing L2 push/deployment approval gates stand.
