---
layout: default
title: MCP setup
permalink: /guides/mcp-setup/
---

# MCP setup

This static site does not operate an MCP service. To use these patterns with a client, obtain a remote MCP endpoint from your deployment operator. Keep the endpoint and credential in the client configuration; template and skill files contain neither.

## Required values

- MCP endpoint: `https://<your-host>/mcp/`
- Authentication: the bearer or OAuth method published by your deployment
- Client support: remote MCP over Streamable HTTP

Keep the trailing slash when the operator publishes one. Some clients drop authorization headers while following redirects.

## Generic client configuration

```json
{
  "mcpServers": {
    "research-wiki": {
      "type": "streamable-http",
      "url": "https://<your-host>/mcp/",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

If your client supports OAuth, use the deployment's authorization flow instead of a static bearer header.

## Session sequence

A conforming client performs:

1. `initialize`
2. `notifications/initialized`
3. `tools/list`
4. `tools/call`

Treat `tools/list` as caller-specific. A server may hide tools whose required scopes are absent.

## First research call

1. Ask the client to describe available research capabilities.
2. Resolve a stable entity identity before requesting company-specific evidence.
3. Start with a discovery or cited-narrative task.
4. Open one returned citation and compare it with the synthesized claim.

## Safe error interpretation

| Symptom | Likely class |
| --- | --- |
| DNS, TLS, timeout, or unsupported media type | Transport |
| `401` or OAuth challenge | Authentication |
| Neutral missing-tool response | Authorization or readiness |
| Typed abstention with limitations | Evidence cannot support the requested claim |
| Partial result | Some bounded work completed; inspect limitations before reuse |

Continue with [agent workflows](agent-workflows.md) for tool-selection guidance.
