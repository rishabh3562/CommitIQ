from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.runnables import RunnableSequence

from configs.prompts import INSIGHT_SUMMARY_TEMPLATE, INSIGHT_SUMMARY_INPUT_VARS,INSIGHT_SUMMARY_INPUT_VARS_V2,INSIGHT_SUMMARY_TEMPLATE_V2

llm = OpenAI(temperature=0.2)
# only for linear flow and not parallel flow
insight_prompt = PromptTemplate(
    input_variables=INSIGHT_SUMMARY_INPUT_VARS,
    template=INSIGHT_SUMMARY_TEMPLATE
)

insight_chain: RunnableSequence = insight_prompt | llm



llm_parallel = OpenAI(temperature=0.2)

# Parallel-safe chain (e.g., for LangGraph shard-aware narrator)
parallel_insight_prompt = PromptTemplate(
    input_variables=INSIGHT_SUMMARY_INPUT_VARS_V2,
    template=INSIGHT_SUMMARY_TEMPLATE_V2
)

parallel_insight_chain: RunnableSequence = parallel_insight_prompt | llm_parallel