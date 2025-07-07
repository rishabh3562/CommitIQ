from .productivity_insight_flow import productivity_insight_flow

slack_workflow = productivity_insight_flow()
# from .productivity_insight_flow import productivity_insight_flow
# from .chunked_parallel_flow import ParallelWorkflowState,run_parallel_flow
# from datetime import datetime, timedelta

# one_week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
# one_month_ago = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
# slack_workflow = productivity_insight_flow()


# # one_week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
#   # create an instance with defaults or params
# # parallel_slack_workflow = run_parallel_flow(initial_state)