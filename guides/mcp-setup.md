---
layout: default
title: MCP setup
permalink: /guides/mcp-setup/
---

# MCP setup

Public documentation and raw skill downloads live at `https://kitkitkittt.github.io/research-wiki/`. The hosted workspace and authenticated MCP endpoint are separate. Keep credentials in the client environment or approved secret store; template and skill files contain none.

## Required values

- Hosted endpoint: `https://research.vnibb.xyz/mcp/research-brain/`
- Deployment-neutral endpoint: `https://<your-host>/mcp/research-brain/`
- Hosted authentication: deployment-issued API-key Bearer token; OAuth is not required or supplied by this setup
- Client support: remote MCP over Streamable HTTP

Keep the trailing slash when the operator publishes one. Some clients drop authorization headers while following redirects.

## Generic client configuration

```json
{
  "mcpServers": {
    "research-wiki": {
      "type": "streamable-http",
      "url": "https://<your-host>/mcp/research-brain/",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

The JSON is a portable source example, not a universal client format. Use the named client's configuration below; configure other clients through their documented secret mechanism.

## Manual Codex setup

Obtain a deployment-issued key with the scopes and lane needed for your task. A principal identifier is not an API key. This manual connection does not require model-provider authorization, provider bootstrap, or an OAuth login.

Add this to your local Codex `~/.codex/config.toml` (replace the host only for another deployment):

```toml
[mcp_servers.research_wiki]
url = "https://research.vnibb.xyz/mcp/research-brain/"
bearer_token_env_var = "VCI_RESEARCH_API_KEY"
```

In Bash, read the key without putting it in shell history, then start Codex from that environment:

```bash
read -rsp 'Deployment API key: ' VCI_RESEARCH_API_KEY; printf '\n'
export VCI_RESEARCH_API_KEY
codex
```

Restart an already-running client after supplying the variable. Do not print the variable or save the key in TOML, the repository, skill files, or prompts. A GUI client must receive the same variable through its approved launch environment.

## Session sequence

A conforming client performs:

1. `initialize`
2. `notifications/initialized`
3. `tools/list`
4. `tools/call`

Treat `tools/list` as caller-specific. A server may hide tools whose required scopes are absent.

## First research call

1. Call `system.describe_capabilities` only if the authenticated `tools/list` exposes it. Its MCP result is `callable-capability-discovery-v1`; the REST runtime matrix is `runtime-capabilities-v1`.
2. Select tools only when current caller-specific discovery reports them callable; static skill `ready` metadata does not prove runtime readiness.
3. For canonical company research, resolve an authorized stable company identity. For retained documents, follow the separately labeled archive workflow in [agent workflows](agent-workflows.md), only if its tools are callable.
4. Complete one authorized evidence search, re-fetch a returned citation, and compare its evidence with the claim. Discovery-only means **connected, research blocked**, not successful research.

## Safe error interpretation

| Symptom | Likely class |
| --- | --- |
| DNS, TLS, timeout, or unsupported media type | Transport |
| `401` or Bearer challenge | Authentication; check the deployment key environment |
| Neutral missing-tool response | Authorization or readiness |
| Typed abstention with limitations | Evidence cannot support the requested claim |
| Partial result | Some bounded work completed; inspect limitations before reuse |

Continue with [agent workflows](agent-workflows.md) for tool-selection guidance.
