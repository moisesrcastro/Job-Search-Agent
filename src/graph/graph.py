from typing import TypedDict, Annotated, List, Optional

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

from src.config import model_config

from src.services.openRouter import OpenRouterService
from src.services.preferencesService import PreferencesService
from src.services.memoryService import create_memory_service

from src.graph.nodes.chatNode import createChatNode
from src.graph.nodes.searchJobsNode import searchJobs
from src.graph.nodes.savePreferencesNode import savePreferencesNode
from src.graph.nodes.summarizationNode import createSummarizationNode

from src.graph.nodes.edgeConditional import (
    route_after_chat,
    route_after_save_preferences
)

openrouter = OpenRouterService(model_config)

preferences_service = PreferencesService()


class JobState(TypedDict):

    messages: Annotated[List[AnyMessage], add_messages]
    is_final_response: bool

    role: Optional[str]

    jobs: list
    jobs_found: bool

    user_id: Optional[str]

    user_context: Optional[str]

    preferences: Optional[dict]

    conversation_summary: Optional[dict]

    extract_preference: bool

    should_search_jobs: bool

    needs_summarization: bool



builder = StateGraph(JobState)

builder.add_node(
    "chat",
    createChatNode(
        openrouter,
        preferences_service
    )
)

builder.add_node(
    "searchJobs",
    searchJobs
)

builder.add_node(
    "savePreferences",
    savePreferencesNode(
        preferences_service
    )
)

builder.add_node(
    "summarize",
    createSummarizationNode(
        openrouter,
        preferences_service
    )
)


builder.add_edge(
    START,
    "chat"
)

builder.add_conditional_edges(
    "chat",
    route_after_chat,
    {
        "savePreferences": "savePreferences",
        "searchJobs": "searchJobs",
        "summarize": "summarize",
        "end": END,
    }
)

builder.add_edge(
    "searchJobs",
    "chat"
)

builder.add_conditional_edges(
    "savePreferences",
    route_after_save_preferences,
    {
        "summarize": "summarize",
        "searchJobs": "searchJobs",
        "end": END,
    }
)

builder.add_edge(
    "summarize",
    END
)


graph = builder.compile(
)