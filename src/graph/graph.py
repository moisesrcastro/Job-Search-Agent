from typing import TypedDict, Annotated, List, Any

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

from src.graph.nodes.identifyJobs import search_jobs
from src.graph.nodes.generateResponse import generate_response


class JobState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    role: str
    jobs: list
    jobs_found: bool

builder = StateGraph(JobState)

builder.add_node("search_jobs", search_jobs)
builder.add_node("generate_response", generate_response)

builder.add_edge(START, "search_jobs")
builder.add_edge("search_jobs", "generate_response")
builder.add_edge("generate_response", END)

graph = builder.compile()

graph = builder.compile()