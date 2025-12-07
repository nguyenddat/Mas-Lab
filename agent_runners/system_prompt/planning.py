from typing import *

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

planning_prompt = """
You are an autonomous research agent controller. You will receive a list of available steps, a list of completed steps and the results of the completed steps. Your task is to review the previous steps and plan the next step to execute.

If the previous steps are verified, you should plan the next step to execute. Also, the next step must be one of the available steps.
If there are no previous steps, you should plan the first step to execute and return verified as True.

Available steps: {available_steps}
Completed steps: {completed_steps}
Results of the previous step: {results_of_previous_step}

Plan the next step to execute and return in JSON format."""

class PlanningResponse(BaseModel):
    verified: bool = Field(..., description="Whether the previous steps are verified")
    next_step: Optional[str] = Field(..., description="The next step to execute")

planning_parser = PydanticOutputParser(pydantic_object=PlanningResponse)
planning_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", planning_prompt + """{format_instructions}"""),
            ("human", "{question}"),
        ]
    ).partial(format_instructions=planning_parser.get_format_instructions())
