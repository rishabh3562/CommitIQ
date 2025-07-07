from configs.constants import NUM_PARALLEL
## agents/batch_collector.py
def batch_collector(state):
    print(f"[COLLECTOR] Received {len(state['diff_results'])} total analyzed results")

    all_results = state.get("diff_results", [])
    return {"analyzed": all_results, "combined": all_results}

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
