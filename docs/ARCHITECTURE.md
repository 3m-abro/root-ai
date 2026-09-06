# ROOT Architecture

## System

YOU
  |
  +-- Web
  +-- Voice
  +-- CLI
  |
  v
ROOT
  |
  v
Hermes
  |
  +-- Personal Execution
  +-- Business Operations
  +-- Research
  +-- Engineering
  +-- Marketing
  +-- Operations
  |
  +-- Leantime
  +-- n8n
  +-- Claude Code
  +-- Local ROOT Agent

## Responsibilities

ROOT
- Decision layer
- Prioritization
- Delegation
- Approval management
- Proactive monitoring
- User execution management

Hermes
- Agent runtime
- Sessions
- Profiles
- Skills
- Delegation
- Memory
- Scheduling

Leantime
- Goals
- Projects
- Tasks
- Milestones
- Business planning

n8n
- Deterministic automation
- External integrations
- Scheduled workflows
- Notifications

Git
- ROOT configuration
- Prompts
- Skills
- Integration code
- Deployment configuration

Runtime state and secrets must remain outside Git.
