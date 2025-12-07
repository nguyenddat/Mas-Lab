import uuid
import logging
from typing import List, Dict, Any

from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_core.tools import Tool

from core import config
from utils.get_models import get_model
from utils.parse_schema import schema_to_pydantic

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, model_name: str, description: str = ""):
        self.agent_id = str(uuid.uuid4())
        self.model_name = model_name

        self.description = description
        self.context: Dict[str, Any] = {}

        self.mcp_server_url = config.MCP_SERVER_URL
    
    def setup(self):
        """Initialize agent, load model, connect tools/MCP."""
        self.model = get_model(self.model_name)
        logger.info(f"Agent {self.agent_id} initialized with model {self.model_name}")
    
    async def get_tools(self):
        if self.mcp_server_url:
            async with sse_client(self.mcp_server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    tools_result = await session.list_tools()
                    return tools_result.tools
        return []
    
    async def mcp_to_openai_tools(self):
        mcp_tools = await self.get_tools()
        tools = []

        for mcp_tool in mcp_tools:
            # Schema for tool calling
            args_schema = schema_to_pydantic(mcp_tool.name, mcp_tool.inputSchema)

            # Function for tool calling
            async def _call_tool(_tool_name=mcp_tool.name, **kwargs):
                return await self.call_tool(_tool_name, kwargs)

            tools.append(
                Tool(
                    name=mcp_tool.name,
                    description=mcp_tool.description,
                    func=_call_tool,
                    args_schema=args_schema
                )
            )
        return tools
    
    async def choose_tool(self, tools, query):
        model_with_tools = self.model.bind_tools(tools)
        response = model_with_tools.invoke(query)
        return response.tool_calls
        
    async def call_tool(self, tool_name: str, args: Dict[str, Any]):
        if self.mcp_server_url:
            async with sse_client(self.mcp_server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    tool_result = await session.call_tool(tool_name, args)
                    return tool_result
        else:
            logger.warning(f"Agent {self.agent_id} cannot call tool {tool_name}: MCP server URL not initialized.")
            return None

    async def run(self, params: Any) -> Any:
        """
        Main entry point for the agent.
        Subclasses should implement this method to define
        how input is processed, which tools to use, and what output to return.
        """
        raise NotImplementedError
    
    async def shutdown(self):
        logger.info(f"Agent {self.agent_id} disconnected from MCP server")