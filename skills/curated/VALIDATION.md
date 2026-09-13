# Static validation evidence

Date: 2026-09-13. Repository base: `ee45eb8`.

The curation check parsed the manifest with PyYAML 6.0.3 using duplicate-key
rejection and parsed Markdown with markdown-it-py CommonMark mode. It compared
original files against the pinned scratch checkouts and curated files against
the recorded SHA-256 values. These are local checks, not runtime safety tests.

| Check | Result |
| --- | --- |
| Requested manifest identities | 11 unique entries, complete expected set |
| Review dispositions | 8 approved static adaptations, 3 deferred |
| Required metadata and immutable revisions | Present; 40-character commit IDs |
| Original and curated Markdown integrity | 18 vendored files checked; deferred entry source hashes also checked |
| Attribution integrity | 4 notice/license files checked |
| Static allowlist | Only listed Markdown, notices, licenses and directory README; no symlinks or executable mode bits |
| Runtime flags | All disabled, runtime validation not run |
| Markdown | CommonMark parse, closed fences and existing relative file links checked |
| Existing regression suite | `python -m unittest discover -v`: 21 tests passed |
| Patch whitespace | `git diff --check`: passed |

The regression suite emitted expected invalid-date CLI output and a Python 3.14
ResourceWarning for an HTTPError cleanup; neither caused a test failure. No
application code or test behavior changed in this curation.

## Revalidation procedure

1. Parse skills-manifest.yaml with a YAML safe loader that rejects duplicate keys.
   Check the 11 names, required fields, boolean flags and decision/path consistency.
2. Retrieve each source at its recorded revision outside a runtime skills path.
   Compute SHA-256 for each `source_path`; compare with `source_sha256`.
3. Compute SHA-256 for each `vendor_path` and attribution file; compare with the
   manifest. Reject unlisted files, symlinks and executable permissions in the pack.
4. Parse approved SKILL.md frontmatter; require matching name and a description.
   Parse Markdown and check fenced blocks and repository-relative file links.
5. Run the existing regression suite and inspect the full staged diff with
   `git diff --cached --check`. Re-review any changed source or curated bytes.

Hermes discovery, tool restriction enforcement, specialist delegation, refusals,
provider behavior and deployment remain untested. Run the documented specialist
pilot before activation; passing static checks cannot substitute for that evidence.
