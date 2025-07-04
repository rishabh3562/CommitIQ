from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.runnables import RunnableSequence

from configs.prompts import INSIGHT_SUMMARY_TEMPLATE, INSIGHT_SUMMARY_INPUT_VARS

llm = OpenAI(temperature=0.2)

insight_prompt = PromptTemplate(
    input_variables=INSIGHT_SUMMARY_INPUT_VARS,
    template=INSIGHT_SUMMARY_TEMPLATE
)

insight_chain: RunnableSequence = insight_prompt | llm
