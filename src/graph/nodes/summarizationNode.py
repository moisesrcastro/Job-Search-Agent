from langchain_core.messages import (
    HumanMessage,
    RemoveMessage
)

from src.services.openRouter import (
    OpenRouterService
)

from src.services.preferencesService import (
    PreferencesService
)

from src.graph.prompts.summarization import (
    SummarySchema,
    get_summarization_system_prompt,
    get_summarization_user_prompt
)

from langgraph.runtime import Runtime


def createSummarizationNode(
    llm_client: OpenRouterService,
    preferences_service: PreferencesService
):

    async def summarizationNode(
        state,
        runtime: Runtime = None
    ):

        conversation_history = [

            {
                "role": (
                    "User"
                    if isinstance(msg, HumanMessage)
                    else "AI"
                ),

                "content": msg.content
            }

            for msg in state["messages"]

        ]

        context = (
            getattr(runtime, "context", None)
            or {}
        )

        previous_summary = await preferences_service.get_summary(
            str(
                context.get(
                    "userId",
                    state.get(
                        "user_id",
                        "unknown"
                    )
                )
            )
        )

        result = await llm_client.generate_structured(

            system_prompt=
                get_summarization_system_prompt(),

            user_prompt=
                get_summarization_user_prompt(
                    conversation_history=
                        conversation_history,

                    previous_summary=
                        previous_summary
                ),

            schema=SummarySchema
        )

        if not result["success"]:

            return {
                "needs_summarization": False
            }

        summary = result["data"]

        context = (
            getattr(runtime, "context", None)
            or {}
                )

        user_id = str(
            context.get(
                "userId",
                "unknown"
            )
        )

        await preferences_service.save_summary(
            user_id=user_id,
            summary=summary.key_preferences
        )

        messages_to_delete = [

            RemoveMessage(
                id=message.id
            )

            for message in state["messages"][:-2]

            if getattr(
                message,
                "id",
                None
            )
        ]

        return {

            "messages":
                messages_to_delete,

            "user_context":
                summary.key_preferences,

            "needs_summarization":
                False
        }

    return summarizationNode