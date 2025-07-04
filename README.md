# CommitIQ

**AI-powered engineering productivity insights, delivered straight to Slack.**
Built for the FIKA AI Research — Engineering-Productivity Intelligence MVP Challenge.

---

## Overview

**CommitIQ** is a chat-first, agent-driven system that provides intelligent engineering insights by analyzing GitHub commit and PR data. It translates raw dev activity into actionable summaries mapped to **DORA metrics**, all delivered through a Slack bot.

* Built with **LangChain + LangGraph**
* Deployed via **Docker** with seeded demo support
* Designed to aid **tech leadership** and **engineering teams** in visibility and performance tracking

---

## Features

* 🧠 Agent-based orchestration (Harvester → Analyst → Narrator)
* 📈 GitHub diff + PR ingestion for per-author metrics
* 📊 Visual + narrative Slack summaries via `/dev-report`
* 🔍 Insight mapping to **DORA’s four keys**
* ⚙️ One-command bootstrapping with seed data
* 🔁 Pluggable and extensible for real-time workflows

---

## Architecture

CommitIQ uses a **LangGraph state machine** to orchestrate agents:

```python
def productivity_insight_flow(seed=False):
    g = StateGraph(WorkflowState)
    g.add_node("harvester", run_data_harvester)
    g.add_node("analyst", run_diff_analyst)
    g.add_node("narrator", run_insight_narrator)
    g.set_entry_point("harvester")
    g.add_edge("harvester", "analyst")
    g.add_edge("analyst", "narrator")
    return g.compile()
```

* **Harvester**: Fetches GitHub events (commits/PRs)
* **Analyst**: Aggregates diffs, calculates churn, flags risks
* **Narrator**: Generates business-facing summaries and charts

> All state transitions are deterministic and composable using LangGraph.

---

Ready for your next section (Setup)?
