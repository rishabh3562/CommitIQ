INSIGHT_SUMMARY_TEMPLATE = (
    "Engineering snapshot:\n"
    "• Deploy freq: {pr_throughput}\n"
    "• Lead time (hrs): {cycle_time}\n"
    "• Change-fail rate: {ci_failures}/{pr_throughput}\n"
    "• MTTR (hrs): {mttr}\n\n"
    "Code metrics:\n"
    "• Commits: {total_commits}\n"
    "• Lines +: {lines_added}  \\-: {lines_deleted}\n"
    "• Files touched: {files_touched}\n\n"
    "Author breakdown:\n{stats}\n\n"
    "Spikes: {spikes}\n\n"
    "Write a 2–3 sentence summary highlighting productivity & bottlenecks."
)

INSIGHT_SUMMARY_INPUT_VARS = [
    "stats", "pr_throughput", "ci_failures", "review_latency", "cycle_time", "spikes",
    "total_commits", "lines_added", "lines_deleted", "files_touched", "mttr"
]
INSIGHT_SUMMARY_INPUT_VARS_V2 = ["dora_summary", "other_summary"]

INSIGHT_SUMMARY_TEMPLATE_V2 = """You are an engineering performance analyst.

## DORA Metrics Summary
{dora_summary}

## Additional Engineering Insights
{other_summary}

Write a concise executive summary highlighting key takeaways from both sections. Be sharp and brief."""
