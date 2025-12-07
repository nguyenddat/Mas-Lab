import asyncio
from typing import Any

from .agent_base import BaseAgent
from utils.get_chat_completion import get_chat_completion
from utils.parse_schema import normalize_mcp_response
from system_prompt.paper_crawl import paper_crawl_prompt, paper_crawl_parser

class AgentPaperCrawler(BaseAgent):
    def __init__(self, model_name, description=""):
        super().__init__(model_name, description)
    
    async def run(self, params: Any) -> Any:
        # Get key queries
        get_key_queries_params = {"question": params["question"]}
        get_key_queries_response = await get_chat_completion(
                self.model,
                paper_crawl_prompt,
                paper_crawl_parser,
                get_key_queries_params
            )

        # Get tools
        tools = await self.mcp_to_openai_tools()    
        
        # Call tool
        results = []
        for key_query in get_key_queries_response["key_queries"]:
            tool_calls = await self.choose_tool(tools, key_query)

            tool_call = tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_response = await self.call_tool(tool_name, tool_args)
            tool_call_response = normalize_mcp_response(tool_call_response)
            results.append(tool_call_response)
        
        return results
