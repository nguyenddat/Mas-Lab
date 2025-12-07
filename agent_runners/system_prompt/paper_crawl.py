from typing import *

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

paper_crawl_prompt = """
You are a paper crawler. You will receive a user query and your task is to crawl Arxiv papers and return the top papers that are most relevant to the query. 

Before retrieving the papers, you must first generate a list of key queries (from 3 to 5) that you will use to search Arxiv. Follow these rules when creating key queries:

1. Key queries should cover different aspects of the user query.
2. Use synonyms and alternative phrasings to increase coverage.
3. Include technical terms or related concepts that appear in recent research.
4. Each key query should be concise (1-3 words if possible) and precise.
5. Avoid including irrelevant or ambiguous terms.

Original query: {question}

Please return the key queries in a list, following the format:
"""

class PaperCrawlResponse(BaseModel):
    key_queries: List[str] = Field(..., description="List of key queries that you will use to search Arxiv")

paper_crawl_parser = PydanticOutputParser(pydantic_object=PaperCrawlResponse)

paper_crawl_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", paper_crawl_prompt + """{format_instructions}"""),
            ("human", "{question}"),
        ]
    ).partial(format_instructions=paper_crawl_parser.get_format_instructions())
