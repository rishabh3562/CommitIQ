from configs.constants import CONCURRENT_WORKERS
## agents/batch_collector.py
def batch_collector(state):
    print(f"[COLLECTOR] Received {len(state['analysis_output'])} total analyzed results")

    all_results = state.get("analysis_output", [])
    return {"processed": all_results, "combined": all_results}

# def batch_collector(state):
#     all_results = []
#     for i in range(1, NUM_PARALLEL + 1):
#         all_results.extend(state.get(f"analyzed_{i}", []))
#     return {"analyzed": all_results}



# def batch_collector(state):
#     return {
#         "analyzed": state.get("analyzed", []),  # or pass forward
#         "combined": state.get("analyzed", [])   # input to aggregator
#     }
