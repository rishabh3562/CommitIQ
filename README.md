

# FIKA AI – Engineering Productivity Intelligence MVP

> 🔍 Turn GitHub activity into DORA-aligned, actionable insights—directly inside Slack.
> ⚙️ Built using LangGraph agents and Python 3.10+, in under 72 hours.

---

## 📑 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Architecture](#architecture)
* [Setup ](#setup-)
* [Usage](#usage)
* [Agents Breakdown](#agents-breakdown)
* [Data Flow](#data-flow)
* [Visualization](#visualization)
* [Prompt Logging](#prompt-logging)
* [Tech Stack](#tech-stack)
* [Contributing / Running Tests](#contributing--running-tests)
* [License](#license)

---

## Overview

FIKA AI is a chat-first, agent-powered productivity analytics tool for engineering teams. It ingests GitHub data and distills it into insights via a Slack bot using DORA metrics.

---

## Features

* 📥 GitHub ingest via REST or seed mode
* 🤖 Agent-based LangGraph pipeline (Harvester → Analyst → Narrator)
* 📊 Slack bot responds with charts + summaries via `/dev-report`
* 🪵 Prompt/response logging for audit
* 🚀 One-command bootstrap (Docker, Makefile)

---

## Architecture

LangGraph-powered, deterministic flow:

```
Harvester (GitHub data)
     ↓
Analyst (diff stats, churn, CI health)
     ↓
Narrator (DORA insights, summary generation)
```

All agents run in a single compiled `StateGraph` flow.

---


## 🔥 Setup

You can run this project in **two ways** — using **Python** or **Docker**.
Pick either one based on your preference (or use both).



### 1. Prepare Your Environment

* **Python version:** 3.10.11

* **Install dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

* **Run the app:**

  ```bash
  python main.py
  ```



### 2. Create Your `.env` File

You’ll find a `.env.sample` file in the repo.
Make a copy and rename it to `.env`.

Fill it with your credentials:

```env
# GitHub
GITHUB_TOKEN=your_github_token
USE_FAKE_DATA=False

# Slack
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_SIGNING_SECRET=...
SLACK_USER_OAUTH_TOKEN=xoxp-...

# OpenAI
OPENAI_API_KEY=sk-...
```



### 3. Slack Bot Setup

1. Go to [Slack API Portal](https://api.slack.com/apps) → Create a new app
2. Enable **Socket Mode**
3. Add a **slash command**: `/dev-report`
4. Paste the Slack credentials in `.env`

📺 Guides:

* [Create Slack Bot & Slash Command](https://www.youtube.com/watch?v=yldme5n3YpM)
   

### 4. GitHub Token Setup

You need a GitHub [Personal Access Token](https://github.com/settings/tokens) with **repo read** permissions.

📺 [Watch setup guide](https://www.youtube.com/watch?v=HbSjyU2vf6Y)

Paste it in your `.env` like:

```env
GITHUB_TOKEN=ghp_...
```



### 5. Run with Docker (Optional)

If you prefer Docker:

```bash
docker-compose up --build
```

> Use `--build` on first run or if requirements change.
> After that, just:

```bash
docker-compose up
```



---

## Usage

Here's your refined **Usage** section, based on your `/dev-report hashicorp terraform` example and previous structure — beginner-friendly, clear, and complete:

---

## 🚀 Usage

Once the bot is running, use these **Slack slash commands** in any channel where the bot is invited:



### ✅ `/dev-report owner repo [options]`

This is the **main command**. It fetches GitHub activity, analyzes productivity, and returns:

* AI-generated summary
* DORA metrics
* PNG charts (optional)

**Examples (using HashiCorp’s Terraform repo):**

```bash
/dev-report hashicorp terraform
/dev-report hashicorp terraform --monthly
/dev-report hashicorp terraform --from 2024-06-01 --to 2024-06-30
/dev-report hashicorp terraform --yesterday
/dev-report hashicorp terraform --no-graph
```

**Optional flags:**

| Flag          | What it does                 |
| ------------- | ---------------------------- |
| `--weekly`    | Default: fetches past 7 days |
| `--monthly`   | Fetches past 30 days         |
| `--from DATE` | Start date in `YYYY-MM-DD`   |
| `--to DATE`   | End date in `YYYY-MM-DD`     |
| `--no-graph`  | Skip charts, summary only    |
| `--help`      | Show command usage           |
| `--yesterday` | Report only for yesterday    |
| `--today`     | Report only for today        |



### 🔁 `/demo-dev-report`

Runs a simulated report using static/sample data — helpful for testing and internal demos.



### ℹ️ `/explain-me`

Shows what the bot does and how to use it.



### 🔄 `/test`

Checks if the bot is active.



* For seeded reports(run python demo.py first): `/demo-dev-report` (uses static data)
* Output includes PNG chart + narrative insight in thread

---

## Agents Breakdown

* **Data Harvester**: Pulls commits, PRs, CI status
* **Diff Analyst**: Calculates code_metrics
* **Insight Narrator**: Outputs natural-language insights, DORA-keyed

---

## Data Flow

1. GitHub data ingested or simulated
2. Diff and churn metrics computed
3. Insights mapped to:

   * Lead time
   * Deployment frequency
   * Change failure rate
   * Mean time to restore

---

## Visualization

* Charts rendered via Plotly and saved as PNGs
* Slack bot posts chart with insight summary in a thread

---

## Prompt Logging

* Each agent logs:

  * Input payload
  * Prompt used
  * Response text
* Logs are written to terminal and optionally stored

---

## Tech Stack

* **LangChain** `== 0.3.26`
* **LangGraph OSS** `== 0.5.0`
* **Slack Bolt (Python)**
* **Plotly** for charting
* **Docker**, `make`, `.env`, `test.py`

---

## Contributing / Running Tests

```bash
make test  # Runs unit tests
```

* Modular code in `agents/`, `bot/`, `services/`
* Use PRs for contributions

---

