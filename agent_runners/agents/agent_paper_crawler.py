import json
import time
import asyncio
from typing import Any

from tqdm import tqdm

from core import logger
from .agent_base import BaseAgent
from utils.get_chat_completion import get_chat_completion
from utils.parse_schema import normalize_mcp_response
from system_prompt import planning_prompt, planning_parser, paper_crawl_prompt, paper_crawl_parser

paper_crawl_agent_steps = ["crawl", "review", "push_database", "done"]
class AgentPaperCrawler(BaseAgent):
    def __init__(self, model_name, description=""):
        super().__init__(
            model_name,
            description,
            steps=paper_crawl_agent_steps
        )
        self.agent_id_short = self.agent_id[:5]
    
    def plan(self, query):
        last_step = self.context["completed_steps"][-1]
        result_of_last_step = self.context["result_of_completed_steps"][last_step][-1]
        params = {
            "question": query,
            "available_steps": self.steps,
            "completed_steps": self.context["completed_steps"],
            "results_of_previous_step": result_of_last_step or ""
        }
        response = get_chat_completion(self.model, planning_prompt, planning_parser, params)
        
        self.context["planned"] = True
        return response

    def get_next_step(self, question):
        # 1. Deterministic transitions (Standard Flow)
        if not self.context["completed_steps"]:
            logger.info(f"[{self.agent_id_short}] Starting deterministic flow. Next step: crawl")
            return {"verified": True, "next_step": "crawl"}
        
        last_step = self.context["completed_steps"][-1]
        
        if last_step == "crawl":
            logger.info(f"[{self.agent_id_short}] Transition: crawl -> review")
            return {"verified": True, "next_step": "review"}
        
        if last_step == "review":
            logger.info(f"[{self.agent_id_short}] Transition: review -> push_database")
            return {"verified": True, "next_step": "push_database"}
        
        if last_step == "push_database":
            logger.info(f"[{self.agent_id_short}] Transition: push_database -> done")
            return {"verified": True, "next_step": "done"}

        # 2. Fallback to LLM Planning for unknown states or error recovery
        logger.info(f"[{self.agent_id_short}] Standard transition not found for {last_step}, falling back to LLM planning...")
        return self.plan(question)

    async def run(self, question: str):
        logger.info(f"[{self.agent_id_short}] Agent started with question: {question}")
        tools = await self.mcp_to_openai_tools()
        logger.info(f"[{self.agent_id_short}] with {len(tools)} tools")
        while self.context["done"] is False:
            # Determine next step (Deterministic > LLM)
            plan = self.get_next_step(question)

            next_step = plan["next_step"]
            
            # If explicit planning (LLM) returned unverified, retry previous
            if plan.get("verified") is False:
                # Assuming fallback to replanning or retrying last step if verified is False
                # But get_next_step mostly returns Verified=True for deterministic.
                # If LLM returns False, we might want to retry previous step.
                next_step = self.context["completed_steps"][-1] if self.context["completed_steps"] else "crawl"

            # Thực hiện next step
            if next_step == "crawl":
                results = await self.crawl(question, tools)

                self.context["completed_steps"].append(next_step)
                self.context["result_of_completed_steps"][next_step].append(results)

            elif next_step == "review":
                results = await self.plan(question)

                self.context["completed_steps"].append(next_step)
                self.context["result_of_completed_steps"][next_step].append(results)

            elif next_step == "push_database":
                results = await self.push_database(question, tools)
                
                self.context["completed_steps"].append(next_step)
                self.context["result_of_completed_steps"][next_step].append(results)

            elif next_step == "done":
                logger.info(f"[{self.agent_id_short}] Agent finished.")
                self.context["done"] = True
    
    async def push_database(self, question, tools):
        results = []
        for result in tqdm(self.context["result_of_completed_steps"]["crawl"][-1], desc=f"[{self.agent_id_short}] Agent pushing paper to database"):
            try:
                query = f"""
                    Push the following paper to database.

                    arxiv_id: {result['arxiv_id']}
                    title: {result['title']}
                    abstract: {result['abstract']}
                    authors: {result['authors']}
                    download_url: {result['download_url']}
                """

                tool_calls = await self.choose_tool(tools, query)
                tool_call = tool_calls[0]
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                tool_call_response = await self.call_tool(tool_name, tool_args)
                tool_call_response = normalize_mcp_response(tool_call_response)

                results.append(tool_call_response)
            except Exception as e:
                if "Duplicate entry" in str(e) or "already exists" in str(e):
                     logger.warning(f"Paper '{result.get('title', 'Unknown')}' already exists in database. Skipping.")
                else:
                    logger.error(f"Error pushing paper '{result.get('title', 'Unknown')}' to database: {e}")
                continue
        return results

    async def crawl(self, question, tools):
        get_key_queries_params = {"question": question}
        get_key_queries_response = await get_chat_completion(
                self.model,
                paper_crawl_prompt,
                paper_crawl_parser,
                get_key_queries_params
            )
        
        results = []
        for key_query in get_key_queries_response["key_queries"]:
            tool_calls = await self.choose_tool(tools, key_query)

            tool_call = tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_response = await self.call_tool(tool_name, tool_args)
            tool_call_response = normalize_mcp_response(tool_call_response)
            
            results += tool_call_response["result"]
        
            logger.info(f"Found total {len(results)} papers of query: {key_query}")
        
        return results