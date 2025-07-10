# Contributing to CommitIQ

Thank you for your interest in contributing to **CommitIQ**!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/commitiq.git
   cd commitiq
   ```

3. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

* Use Python 3.10+

* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

* Run locally:

  ```bash
  python main.py
  ```

Or with Docker:

```bash
docker-compose up --build
```


## Submitting a Pull Request

1. Make sure your code follows existing style.
2. Include relevant tests or updates.
3. Submit a pull request with a clear description.

## Code Structure

* `agents/`: LangGraph agents (Harvester, Analyst, Narrator)
* `bot/`: Slack integration
* `services/`: GitHub and utility logic

---

Need help? Open an issue or reach out via [LinkedIn](https://www.linkedin.com/in/rishabh108/).