import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from utils import logger, parse_flags, iso_now_minus, dt_parse
from viz import plot_individual_graphs
from workflow.parallel_flow_v2 import build_graph_parallel_v2
from schemas.parallel_workflow_state import ParallelWorkflowStateV2 as State
from utils.common.safe_slack_call import safe_slack_call
from configs.slack_v2 import app, socket_handler
load_dotenv()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# from configs.slack_v1 import app, socket_handler

graph = build_graph_parallel_v2(State)

def schedule_next(client, channel, owner, repo, period):
    days = 7 if period == "weekly" else 30
    post_at = int((datetime.utcnow() + timedelta(days=days)).timestamp())
    client.chat_scheduleMessage(
        channel=channel,
        post_at=post_at,
        text=f"⏰ Auto–reminder: `/dev-report {owner} {repo} --{period}`"
    )

async def run_report(client, channel, user, owner, repo, since, until, flags):
    result = await graph.ainvoke({
        "owner": owner,
        "repo": repo,
        "since": since,
        "until": until,
    })

    agg           = result.get("aggregated", {})
    dora          = result.get("dora", {})
    other_summary = result.get("other_summary", "")
    llm_summary   = result.get("llm_summary", "")
    stats         = agg.get("authors", {})

    # Build blocks
    blocks = [
        # AI Summary
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📌 AI Summary:*\n{llm_summary or 'No summary.'}"
            }
        },
        {"type": "divider"},

        # DORA Metrics
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*📊 DORA Metrics*"},
            "fields": [
                {"type": "mrkdwn", "text": f"*Deploys:*\n{dora.get('deploy_count',0)}"},
                {"type": "mrkdwn", "text": f"*CI Failures:*\n{dora.get('ci_failures',0)}"},
                {"type": "mrkdwn", "text": f"*Lead Time (hrs):*\n{dora.get('avg_lead_time_hours',0):.2f}"},
                {"type": "mrkdwn", "text": f"*Review Latency (hrs):*\n{dora.get('avg_review_latency_hours',0):.2f}"},
                {"type": "mrkdwn", "text": f"*Cycle Time (hrs):*\n{dora.get('avg_cycle_time_hours',0):.2f}"},
                {"type": "mrkdwn", "text": f"*Fail Rate:*\n{dora.get('change_failure_rate',0):.2%}"},
                {"type": "mrkdwn", "text": f"*MTTR (hrs):*\n{dora.get('mttr_hours',0):.2f}"}
            ]
        },
        {"type": "divider"},

        # Repo Summary
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📦 Repo Summary:*\n{other_summary or 'No data.'}"
            }
        },
        {"type": "divider"},
    ]

    # # Per-author avatars
    # if stats:
    #     avatars = []
    #     for author in list(stats.keys())[:10]:  # Only top 10 authors
    #         avatars.append({
    #             "type": "image",
    #             "image_url": f"https://avatars.githubusercontent.com/{author}",
    #             "alt_text": author
    #         })
    #     blocks.append({"type": "context", "elements": avatars})

        # blocks.append({"type": "divider"})

    # Refresh button + footer
    blocks += [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Refresh 🔄"},
                    "action_id": "refresh_report",
                    "value": f"{owner}|{repo}|{since}|{until}|{flags.get('period','')}"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"_Report for `{owner}/{repo}` from {since[:10]} to {until[:10] if until else 'now'}_"
                }
            ]
        }
    ]

    # Post summary
    client.chat_postMessage(channel=channel, blocks=blocks, text="✅ Dev Report ready!")

    # Upload graphs
    if flags.get("graph", True) and stats:
        img_dict = plot_individual_graphs(stats)
        uploads = [{
            "file": buf,
            "filename": name,
            "title": name.replace("_", " ").title()
        } for name, buf in img_dict.items()]
        client.files_upload_v2(channel=channel,
                               initial_comment="📈 Author Contributions",
                               file_uploads=uploads)

    # Auto‑reschedule
    if flags.get("period") in ("weekly", "monthly"):
        schedule_next(client, channel, owner, repo, flags["period"])

@app.command("/monday-drop")
def handle_monday_drop(ack, body, client, command):
    ack()
    user   = body["user_id"]
    ch     = body["channel_id"]
    text   = command["text"].strip()
    parts  = text.split()

    if len(parts) < 2:
        return client.chat_postEphemeral(channel=ch, user=user, text="❌ Usage: `/monday-drop owner repo`")

    owner, repo = parts[0], parts[1]

    now = datetime.utcnow()
    last_monday = now - timedelta(days=now.weekday())
    next_monday = last_monday + timedelta(days=7)

    since = last_monday.isoformat()
    until = now.isoformat()

    loader = client.chat_postMessage(channel=ch, text=":hourglass_flowing_sand: Running Monday drop…")
    asyncio.run(run_report(client, ch, user, owner, repo, since, until, {"period": "weekly"}))
    client.chat_update(channel=ch, ts=loader["ts"], text="✅ Monday drop complete!")

@app.command("/dev-report")
def handle_dev_report(ack, body, client, command):
    ack()
    user   = body["user_id"]
    ch     = body["channel_id"]
    text   = command["text"].strip()
    flags  = parse_flags(text)

    if flags.get("help"):
        return client.chat_postEphemeral(
            channel=ch, user=user,
            text="Usage: `/dev-report owner repo [--weekly|--monthly] [--from YYYY-MM-DD --to YYYY-MM-DD] [--no-graph]`"
        )

    parts = text.split()
    if len(parts) < 2:
        return client.chat_postEphemeral(channel=ch, user=user, text="❌ Provide `owner repo`")

    owner, repo = parts[0], parts[1]
    if flags["from"] and flags["to"]:
        since = dt_parse(flags["from"]).isoformat()
        until = dt_parse(flags["to"]).isoformat()
    else:
        days = 30 if flags["period"] == "monthly" else 7
        since = iso_now_minus(days)
        until = None

    loader = client.chat_postMessage(channel=ch, text=":hourglass_flowing_sand: Generating report…")
    logger.set_slack_logger(lambda msg: client.chat_postMessage(channel=ch, text=msg))

    # kick off
    asyncio.run(run_report(client, ch, user, owner, repo, since, until, flags))

    # update loader
    client.chat_update(channel=ch, ts=loader["ts"], text="✅ Report ready!")


@app.action("refresh_report")
def handle_refresh(ack, body, client):
    ack()
    channel = body["channel"]["id"]
    user    = body["user"]["id"]
    owner, repo, since, until, period = body["actions"][0]["value"].split("|")
    # re‑run exactly the same way
    asyncio.run(run_report(client, channel, user, owner, repo, since, until or None, {"period": period}))

@app.command("/test")
def handle_test(ack, say, command):
    ack()
    say("✅ v2 Slack bot is running!")

@app.command("/explain-me")
def handle_help(ack, say, command):
    ack()
    say(
        "*🤖 Dev Report Bot v2 Help*\n\n"
        "`/dev-report owner repo [--weekly|--monthly] [--from YYYY-MM-DD --to YYYY-MM-DD] [--no-graph]`\n"
        "`/test` → Bot status\n"
        "`/explain-me` → Show this help\n\n"
        "⏰ Schedule `/dev-report` weekly for best insights."
    )

@app.event("app_mention")
def mention_handler(event, say):
    say("👋 Yes, I'm listening.")

@app.error
def global_error_handler(error, body, logger):
    logger.error(f"[Slack Bot Error] {error}")
def run_v2():
    print("[V2] Starting bot in Socket Mode...")
    socket_handler.start()  