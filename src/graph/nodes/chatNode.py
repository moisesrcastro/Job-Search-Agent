from langchain_core.messages import AIMessage
from src.graph.prompts.chatResponse import (
    ChatResponseSchema,
    get_system_prompt,
    get_user_prompt
)


def createChatNode(openrouter, preferences_service):

    async def chatNode(state, runtime):

        context = getattr(runtime, "context", None)

        if isinstance(context, dict):
            user_id = str(context.get("user_id", "unknown"))
        else:
            user_id = "unknown"

        user_context = state.get("user_context")

        if not user_context:
            user_context = await preferences_service.get_summary(user_id)

        last_message = state["messages"][-1].content

        jobs = state.get("jobs", [])
        jobs_found = state.get("jobs_found", False)

        result = await openrouter.generate_structured(
            system_prompt=get_system_prompt(
                user_context=user_context,
                jobs=jobs
            ),
            user_prompt=get_user_prompt(
                question=last_message,
                conversation_history=state["messages"]
            ),
            schema=ChatResponseSchema
        )

        if not result["success"]:
            return {
                "extract_preference": False,
                "should_search_jobs": False,
                "needs_summarization": False,
                "user_context": user_context
            }

        response = result["data"]

        should_search_jobs = bool(response.shouldSearchJobs) and not jobs_found

        next_state = {
            "user_context": user_context,
            "role": (
                response.preferences.role
                if response.preferences
                else state.get("role")
            ),
            "extract_preference": bool(response.shouldSavePreferences),
            "should_search_jobs": should_search_jobs,
            "needs_summarization": len(state["messages"]) >= 6
        }

        if jobs_found:
            if jobs:
                next_state["messages"] = [
                    AIMessage(content=response.message)
                ]
            else:
                next_state["messages"] = [
                    AIMessage(
                        content="Não foram encontradas vagas para os critérios informados no momento. Você pode ajustar filtros como cargo, senioridade ou localização."
                    )
                ]
        else:
            next_state["messages"] = [
                AIMessage(content=response.message)
            ]

        return next_state

    return chatNode