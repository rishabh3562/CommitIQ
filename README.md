# **CommitIQ – Engineering Productivity Insights**

> 📊 Transform GitHub activity into DORA-aligned insights directly in Slack
> ⚙️ Powered by LangGraph agents and Python 3.10+

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Agents](#agents)
- [Data Flow](#data-flow)
- [Visualization](#visualization)
- [Prompt Logging](#prompt-logging)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**CommitIQ** is an agent-based engineering intelligence bot that integrates GitHub with Slack, providing real-time DORA metrics and performance summaries.

---

## Features

- 📥 GitHub ingest (live or static)
- 🧠 LangGraph-based agent pipeline
- 🧾 Slack slash commands with narrative + charts
- 🔍 Auditable prompt logging
- ⚡ Docker-first, one-command deploy

---

## Architecture

```
start_node
   ↓
harvester_orchestrator
   ↓↘︎↘︎↘︎      (parallel)
harvester_i → diff_analyst_i
   ↘︎↘︎↘︎
batch_collector
   ↓
aggregator
   ↓
narrator
   ↓
slack_reporter
```

Each `harvester_i` and corresponding `diff_analyst_i` node runs in **parallel**, managed by `harvester_orchestrator`. All analysis results are merged via `batch_collector` before aggregation and insight narration.

---

## Setup

### 1. Python Setup

```bash
pip install -r requirements.txt
python main.py
```

### 2. Docker Setup

```bash
docker-compose up --build  # First time
docker-compose up          # Subsequent runs
```

### 3. Create `.env` from `.env.sample`

Fill in your keys:

```env
# GitHub
GITHUB_TOKEN=ghp_xxx                  # GitHub personal access token with repo read access

#only in v1 (not used though but good to have this)
USE_FAKE_DATA=False

# Slack
SLACK_BOT_TOKEN=xoxb-xxx              # Slack bot token
SLACK_APP_TOKEN=xapp-xxx              # Slack app-level token (for Socket Mode)
SLACK_SIGNING_SECRET=xxxx             # Slack signing secret

# OpenAI (or other LLM)
OPENAI_API_KEY=sk-xxx                 # Required if you're using OpenAI

# LangSmith Configuration (Optional)
LANGSMITH_TRACING=true                 # Enable LangSmith tracing
LANGSMITH_API_KEY=ls_xxx              # LangSmith API key
LANGSMITH_PROJECT=commitiq-productivity # Project name in LangSmith
LANGSMITH_ENDPOINT=https://api.smith.langchain.com # LangSmith endpoint
```

---

## Usage

### ✅ `/dev-report owner repo [options]`

Generates AI-powered GitHub report with:

- DORA metrics
- PNG chart
- Narrative summary

**Examples:**

```bash
/dev-report hashicorp terraform
/dev-report hashicorp terraform --monthly
/dev-report hashicorp terraform --from 2024-06-01 --to 2024-06-30
```

**Optional Flags:**

| Flag          | Description               |
| ------------- | ------------------------- |
| `--weekly`    | Past 7 days (default)     |
| `--monthly`   | Past 30 days              |
| `--from DATE` | Start date                |
| `--to DATE`   | End date                  |
| `--yesterday` | Report for yesterday only |
| `--today`     | Report for today only     |
| `--no-graph`  | Text summary only         |

---

## Agents

- **start_node** – Initializes the state
- **harvester_orchestrator** – Launches parallel data collectors
- **data_collector_i** – Fetches GitHub commits in segments
- **code_reviewer_i** – Reviews code changes per segment
- **batch_collector** – Merges results from all reviewers
- **aggregator** – Computes DORA and code metrics
- **narrator** – Generates summaries and insights
- **slack_reporter** – Sends results to Slack

---

## Data Flow

1. GitHub data collected in shards
2. Each shard is analyzed for diffs and churn
3. All results collected, aggregated, and summarized
4. Report posted to Slack with chart and narrative

---

## Visualization

- Charts rendered using `matplotlib`
- Sent as PNG in Slack threads

---

## Prompt Logging

- Inputs, prompts, and responses are logged
- Optional file-based logging support
- **LangSmith Integration**: Automatic tracing of LLM interactions when configured

---

## Tech Stack

- **LangChain** `0.3.26`
- **LangGraph OSS** `0.5.0`
- \*\*Slack Bolt (Python)\`
- **matplotlib**, **Docker**, **Python 3.10+**

---

## Contributing

PRs welcome — this repository follows formal open-source standards:

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Issue Template](./ISSUE_TEMPLATE.md)
- [Security Policy](./SECURITY.md)

Please review them before contributing or reporting issues.

---

## License

[MIT License](LICENSE)
