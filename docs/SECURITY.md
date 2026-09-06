# ROOT Security Model

## Principles

- Least privilege
- Explicit capabilities
- Separate control plane from execution environments
- Secrets never committed to Git
- Sensitive actions require approval
- Prefer reversible actions
- Maintain auditability

## Environments

### VPS

Runs:
- ROOT
- Hermes
- Leantime integration
- n8n integration
- AI workers

### Local PC

Runs:
- Cursor
- Claude Code
- development projects
- local ROOT agent
- Docker
- GPU workloads

The VPS must not receive unrestricted administrator access to the PC.

## Secrets

Never commit:
- API keys
- passwords
- OAuth tokens
- SSH private keys
- session databases
- production credentials

Use environment variables, secret stores, or protected runtime configuration.

## Git

Never commit:
- .env
- credentials
- runtime state
- logs containing secrets
- production databases
- Hermes private session state
- n8n credential exports containing secrets

## Production

Production changes require explicit approval unless a specific automation has been deliberately authorized.
