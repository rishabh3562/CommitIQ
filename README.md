# **CommitIQ – Engineering Productivity Insights**

> 📊 Transform GitHub activity into DORA-aligned insights directly in Slack
> ⚙️ Powered by LangGraph agents and Python 3.10+

---

## 📑 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Architecture](#architecture)
* [Setup](#setup)
* [Usage](#usage)
* [Agents](#agents)
* [Data Flow](#data-flow)
* [Visualization](#visualization)
* [Prompt Logging](#prompt-logging)
* [Tech Stack](#tech-stack)
* [Contributing / Testing](#contributing--testing)
* [License](#license)

---

## Overview

**CommitIQ** is an agent-based engineering intelligence bot that integrates GitHub with Slack, providing real-time DORA metrics and performance summaries.

---

## Features

* 📥 GitHub ingest (live or static)
* 🧠 LangGraph-based agent pipeline
* 🧾 Slack slash commands with narrative + charts
* 🔍 Auditable prompt logging
* ⚡ Docker-first, one-command deploy

---

## Architecture

```
Harvester (GitHub data)
     ↓
Analyst (diff stats, churn, CI health)
     ↓
Narrator (DORA insights, summary generation)
```

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

#only in v1(not used though but good to have this)
USE_FAKE_DATA=False

# Slack
SLACK_BOT_TOKEN=xoxb-xxx              # Slack bot token
SLACK_APP_TOKEN=xapp-xxx              # Slack app-level token (for Socket Mode)
SLACK_SIGNING_SECRET=xxxx             # Slack signing secret

# OpenAI (or other LLM)
OPENAI_API_KEY=sk-xxx                 # Required if you're using OpenAI

# Optional - if using LangGraph/chain-specific services
LANGCHAIN_API_KEY=xxx                 # If using LangSmith for logging/tracing

```

---

## Usage

### ✅ `/dev-report owner repo [options]`

Generates AI-powered GitHub report with:

* DORA metrics
* PNG chart
* Narrative summary

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

* **Harvester** – Fetches commits, PRs, CI data
* **Analyst** – Calculates diffs and churn
* **Narrator** – Summarizes findings using DORA metrics

---

## Data Flow

1. GitHub data collected
2. Code-level stats computed
3. Insights generated for:

   * Lead time
   * Deployment frequency
   * Change failure rate
   * Mean time to restore

---

## Visualization

* Charts rendered using matplotlib
* Sent as PNG in Slack thread

---

## Prompt Logging

* Inputs, prompts, responses logged
* Optional file logging enabled

---

## Tech Stack

* **LangChain** `0.3.26`
* **LangGraph OSS** `0.5.0`
* **Slack Bolt (Python)**
* **matplotlib**, **Docker**

---

## Contributing

PRs welcome — this repository follows formal open-source standards:

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Issue Template](.github/ISSUE_TEMPLATE.md)
- [Security Policy](./SECURITY.md)

Please review them before contributing or reporting issues.

---

## License

[MIT License](LICENSE)



