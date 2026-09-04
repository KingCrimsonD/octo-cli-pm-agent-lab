# Cloud Agent Bootstrap

These files are designed for cloud-hosted Agents that cannot access the local workspace.

## Agent A

Use `agents/agent-a-product-steward.md` as the full system / instruction document for the public-facing product steward Agent.

Raw URL:

```text
https://raw.githubusercontent.com/KingCrimsonD/octo-cli-pm-agent-lab/main/agents/agent-a-product-steward.md
```

## Agent B

Use `agents/agent-b-pm-reviewer.md` as the full system / instruction document for the PRD / PM review Agent.

Raw URL:

```text
https://raw.githubusercontent.com/KingCrimsonD/octo-cli-pm-agent-lab/main/agents/agent-b-pm-reviewer.md
```

## Required cloud environment variables / secrets

```env
GITHUB_REPO=KingCrimsonD/octo-cli-pm-agent-lab
GITHUB_TOKEN=<store only as secret, never paste into prompt>
MAIN_EXAMINER_ID=
OCTO_GROUP_ID=
AGENT_A_NAME=octo-cli 产品管家
AGENT_B_NAME=octo-cli PM Reviewer
OCTO_CLI_SOURCE_REPO=https://github.com/Mininglamp-OSS/octo-cli
KNOWLEDGE_BASE_REPO=https://github.com/KingCrimsonD/octo-cli-pm-agent-lab
```

Do not commit `.env` or expose any token in chat, issue body, PRD, logs, or markdown.
