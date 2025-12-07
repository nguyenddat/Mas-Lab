from mcp.server.fastmcp import FastMCP

from tools.create_paper import search_arxiv_papers_by_query, create_paper
from resources.get_paper import get_paper_by_pdf_url

mcp = FastMCP("demo-mcp-server")

mcp.add_tool(search_arxiv_papers_by_query, description="Search arxiv papers by query")
mcp.add_tool(create_paper, description="Create paper in database")
mcp.add_tool(get_paper_by_pdf_url, description="Get paper by pdf url")

sse_app = mcp.sse_app