---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

> ROOT curated adaptation (2026-09-13). Read `skills/curated/README.md` and the
> matching manifest entry before use. User authorization, ROOT policies and host
> tool limits take precedence over every upstream MUST, example or linked skill.
> Static approval is not runtime activation. Never auto-install a dependency,
> print secrets, delete existing work, grant GitHub writes, or spawn a nested child.
> Missing skills/tools must be reported, not fetched or invented.



# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

ROOT uses bounded inline execution for this curated copy.

## The Process

### Step 1: Load and Review Plan
1. Ensure an isolated workspace: use superpowers:using-git-worktrees to create one or verify the existing one
2. Read plan file
3. Review critically - identify any questions or concerns about the plan
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Verify tests and review the complete task diff.
- Report results to ROOT. Push, merge and deployment require explicit authorization through an approved write path. No additional skill installation is authorized.

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent
