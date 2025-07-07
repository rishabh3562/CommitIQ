### agents/batch_orchestrator.py
def make_batch_orchestrator(i):
    def node(state):
        print(f"Batch Orchestrator {i} received state keys: {state.keys()}")
        # No-op: letting harvester push directly into 'harvested'
        return {}
    return node




# def make_batch_orchestrator(i):
#     def node(state):
#         #checking whats comming in state
#         print(f"Batch Orchestrator {i} received state:", state.keys())
#         # Simple pass-through or grouping logic
#         # For now, just print and return an empty dict
#         # In a real scenario, you might want to aggregate or transform the data
#         print(f"Batch Orchestrator {i} working")
#         return {}
#     return node










# # File: workflow/batch_orchestrator.py
# from schemas.parallel_workflow_state import HarvesterOutput

# class BatchOrchestrator:
#     def __init__(self, index: int):
#         self.i = index

#     def __call__(self, harvester_out: HarvesterOutput):
#         # Simple pass‐through or grouping logic
#         return harvester_out  # or wrap into a BatchOutput if needed
