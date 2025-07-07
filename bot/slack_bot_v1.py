import os
from configs.slack_v1 import app,socket_handler
from utils import logger,parse_flags,iso_now_minus,dt_parse
from workflow import slack_workflow
from viz import plot_individual_graphs


@app.command("/dev-report")
def handle_report(ack, body, client, command):
    ack()
    user = body["user_id"]
    ch = body["channel_id"]
    text = command["text"].strip()

    flags = parse_flags(text)
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
        days = 7 
        if flags["period"] == "monthly":
            days = 30
        elif flags["period"] == "weekly":
            days = 7

        since = iso_now_minus(days=days)
        until = None
    

    loader = client.chat_postMessage(channel=ch, text=":hourglass_flowing_sand: Generating report… this may take a few minutes.")

    def slack_logger(msg):
        client.chat_postMessage(channel=ch, text=msg)

    logger.set_slack_logger(slack_logger)

    try:
        logger.terminal_log(f"[SLACK] Running report for {owner}/{repo}")
        out = slack_workflow.invoke({"owner": owner, "repo": repo, "since": since})
        logger.terminal_log("[SLACK] Workflow complete.")

        try:
            stats   = out["analyst"]["author_stats"]
            summary = out["narrator"]["summary"]
            doras   = out["harvester"]
            narrator = out["narrator"]
        except KeyError:
            return client.chat_postEphemeral(
                channel=ch, user=user,
                text="⚠️ Report generation incomplete—missing intermediate data."
            )

        if not stats or not summary:
            raise KeyError("Missing stats or summary in workflow output")

        blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text":
                    f"*Summary:*\n{summary}\n\n"
                    f"*DORA Metrics:*\n"
                    f"> Deploy freq: {doras['pr_throughput']}  |  "
                    f"Lead time: {doras['cycle_time']}h  |  "
                    f"Fail rate: {doras['ci_failures']}/{doras['pr_throughput']}  |  "
                    f"MTTR: {out['narrator']['stats'].get('mttr', 'n/a')}h\n\n"
                    f"*Code Stats:*\n"
                    f"> Commits: {out['narrator']['stats']['total_commits']}  |  "
                    f"+{out['narrator']['stats']['lines_added']}/-{out['narrator']['stats']['lines_deleted']} lines  |  "
                    f"{out['narrator']['stats']['files_touched']} files"
                    
            }
        }]

        if flags["graph"]:
            img_dict = plot_individual_graphs(stats)

            uploads = []
            for filename, file_buf in img_dict.items():
                uploads.append({
                    "file": file_buf,
                    "filename": filename,
                    "title": filename.replace("_", " ").title().replace(".Png", "")
                })

            client.files_upload_v2(
                channel=ch,
                initial_comment="📊 Developer Productivity Visuals",
                file_uploads=uploads
            )

        client.chat_postMessage(channel=ch, blocks=blocks, text="Here's your report summary")
        client.chat_update(channel=ch, ts=loader["ts"], text="✅ Report ready!")

    except Exception:
        import traceback
        traceback.print_exc()
        client.chat_postEphemeral(
            channel=ch, user=user,
            text="⚠️ Failed to generate report. See logs for details."
        )


@app.command("/test")
def handle_test(ack, say, command):
    try:
        ack()
        say(f"✅ Bot is live!")
    except Exception as e:
        say(f"⚠️ Test command failed.\nError: `{str(e)}`")

@app.command("/explain-me")
def handle_explain(ack, say, command):
    try:
        ack()
        say(
            "*👋 Welcome to Dev Report Bot!*\n\n"
            "*What this bot does:*\n"
            "Provides weekly GitHub commit analysis, visual metrics, and DORA-based summaries.\n\n"
            "*Commands:*\n"
            "• `/dev-report owner repo` → Generate a dev report\n"
            "• `/test` → Check bot status\n"
            "• `/explain-me` → Help guide\n\n"
            "Output: stats, PNG graph, AI-generated summary.\n"
            "_Tip: Schedule this weekly._"
        )
    except Exception as e:
        say(f"⚠️ Failed to explain bot usage.\nError: `{str(e)}`")

@app.error
def handle_errors(error, body, logger):
    logger.error(f"Global error: {error}")

@app.event("app_mention")
def log_event(event, say):
    print("EVENT:", event)
    say("👀 Bot is alive and listening.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)
    print("Starting bot in Socket Mode...")
    socket_handler.start()


def run_v1():
    print("[V1] Starting bot in Socket Mode...")
    socket_handler.start()

