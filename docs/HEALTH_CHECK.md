# ROOT Service Health-Check Specification

## Purpose
This document defines the health-check endpoints for a future ROOT service. Health-checks are used to determine service availability and readiness for traffic.

## Endpoints

### Liveness
- **Endpoint**: `GET /health/live`
- **Purpose**: Checks if the Hermes agent process is responsive and the internal event loop is not blocked.
- **Success Response**: Returns HTTP 200 if the Hermes agent process is responsive and the internal event loop is not blocked (indicating the service can recover from failure if restarted).
- **Failure Response**: Returns HTTP 503 if the Hermes agent process is unresponsive or the internal event loop is blocked (indicating the service requires restart).

### Readiness
- **Endpoint**: `GET /health/ready`
- **Purpose**: Checks if the service is ready to serve traffic by verifying critical dependencies.
- **Success Response**: Returns HTTP 200 only when all critical dependencies are reachable and respond within their SLA thresholds (defined below).
- **Failure Response**: Returns HTTP 503 if any dependency is unavailable or exceeds its SLA threshold.

## Response Format
Both endpoints return a JSON object with the following fields:
- `status`: string - overall status ("healthy", "unhealthy", "degraded")
- `timestamp`: string - ISO 8601 timestamp of the check
- `checks`: array of objects, each representing a dependency check:
  - `name`: string - name of the dependency
  - `status`: string - "pass", "fail", "warning"
  - `latency_ms`: number - latency in milliseconds (optional in production to reduce information disclosure)
  - `error`: string (optional) - sanitized error message if check failed (should not contain sensitive information)

Mapping between HTTP status and JSON status:
- HTTP 200: JSON status may be "healthy" or "degraded" (if any warnings but all required checks pass)
- HTTP 503: JSON status is "unhealthy"

## Dependencies and SLA Thresholds
Readiness depends on the following critical systems, each with an SLA threshold:
- **Leantime RPC endpoint**: HTTP GET to `/api/health` (or equivalent) with header `x-root-api-key`; SLA ≤ 200ms.
- **n8n allowlisted gateway**: HTTP GET to `/health`; SLA ≤ 200ms.
- **Local file system access**: Ability to read the skills directory (`skills/`); SLA ≤ 50ms.
- **Hermes skill repository availability**: Check that the skills directory contains at least one skill file; SLA ≤ 50ms.

## Failure Behavior
- Liveness failure indicates the service process itself is unhealthy and should be restarted.
- Readiness failure indicates the service cannot serve traffic but may recover if dependencies are restored.
- Health-checks should not cascade failures; they should be lightweight and fast.
- If a health-check endpoint itself fails to respond, the service is considered completely unavailable.
- Implementation should include timeouts per dependency (as per SLA), circuit breaker pattern (e.g., after 5 consecutive failures, temporarily assume unhealthy for 30 seconds), and no caching of results.

## Configuration and Operational Notes
- The health-check endpoints should be bound only to `127.0.0.1:9119` (accessible via Tailscale) as per ARCHITECTURE.md.
- Authentication: The endpoint should require a valid internal token (e.g., from environment variable or secrets manager) to prevent unauthorized access.
- Rate limiting: Implement rate limiting (e.g., 10 requests per second per client) to prevent denial‑of‑service.
- Error messages in the `error` field must be sanitized to exclude stack traces, connection strings, or other internal details.
- Consider omitting non‑essential fields like `latency_ms` and detailed `error` from external responses in production to reduce information leakage.
- Health‑checks should be performed at a configured interval (e.g., every 10 seconds) by an external monitoring system.

---
*This is a documentation-only specification for future implementation.*