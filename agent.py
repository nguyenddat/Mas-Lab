import asyncio
import os
import json

from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
MCP_SERVER_URL = "http://localhost:8001/sse"
OPENAI_MODEL = "gpt-3.5-turbo"

async def main():
    user_query = "agentic coding"
    print(f"User Query: {user_query}")

    client = AsyncOpenAI()

    print(f"Connecting to MCP server at {MCP_SERVER_URL}...")
    try:
        async with sse_client(MCP_SERVER_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # List tools
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"Connected to MCP Server. Available tools: {[t.name for t in tools]}")

                # Prepare tools for OpenAI function calling
                openai_tools = []
                for t in tools:
                    openai_tools.append({
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description or "",
                            "parameters": t.inputSchema
                        }
                    })

                # Ask GPT to decide which tool to call
                response = await client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a research assistant. Use the available tools to help the user."},
                        {"role": "user", "content": user_query}
                    ],
                    tools=openai_tools,
                    tool_choice="auto"
                )

                choice = response.choices[0]
                if choice.message.tool_calls:
                    for tool_call in choice.message.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = tool_call.function.arguments
                        print(f"  -> Decided to call: {fn_name} with args: {fn_args}")

                        try:
                            args_dict = json.loads(fn_args)
                            # Limit max_results if searching arxiv
                            if fn_name == "search_arxiv_papers_by_query":
                                args_dict["max_results"] = min(args_dict.get("max_results", 5), 5)
                            print(f"  -> Decided to call: {fn_name} with args (after limit): {args_dict}")
                            tool_result = await session.call_tool(fn_name, args_dict)
                            # Call the tool safely
                            try:
                                tool_result = await session.call_tool(fn_name, args_dict)
                            except Exception as e:
                                print(f"⚠️ Error calling tool {fn_name}: {e}")
                                tool_result = None

                            if tool_result is not None:
                                print(f"  -> Tool Output: {tool_result.content}")
                            else:
                                print(f"  -> Tool {fn_name} returned no result")

                            # Optional: feed back to GPT for summary
                            if tool_result is not None:
                                final_response = await client.chat.completions.create(
                                    model=OPENAI_MODEL,
                                    messages=[
                                        {"role": "system", "content": "Summarize the findings based on the tool output."},
                                        {"role": "user", "content": f"User Request: {user_query}"},
                                        {"role": "function", "name": fn_name, "content": str(tool_result.content)}
                                    ]
                                )
                                print("\n=== Final Answer ===")
                                print(final_response.choices[0].message.content)

                        except Exception as e:
                            print(f"⚠️ Error processing tool call {fn_name}: {e}")

                else:
                    print("Agent decided not to use any tools.")
                    print(choice.message.content)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())