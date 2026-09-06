# Local ROOT Agent

The Local ROOT Agent provides controlled execution on the user's PC.

It is the security boundary between the VPS and the local machine.

## Responsibilities

- execute approved commands
- interact with local development environments
- invoke Claude Code
- interact with Git
- run tests
- manage Docker
- access approved local directories

## Security

The local agent must:

- run with least privilege
- expose explicit capabilities
- reject unauthorized commands
- maintain an audit trail
- never expose arbitrary shell access
- never expose credentials unnecessarily

ROOT must not obtain unrestricted remote shell access to the user's PC.
