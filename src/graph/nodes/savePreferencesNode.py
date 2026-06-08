from langgraph.runtime import Runtime

from src.services.preferencesService import (
    PreferencesService
)


def savePreferencesNode(preferences_service: PreferencesService):

    async def save_preferences_node(state, runtime: Runtime = None):

        context = getattr(runtime, "context", None) or {}

        user_id = str(context.get("user_id", "unknown"))

        preferences = state.get("preferences")

        if not preferences:
            preferences = {
                "role": state.get("role"),
                "location": state.get("location"),
                "seniority": state.get("seniority"),
                "company": state.get("preferred_companies"),
                "remote": state.get("remote"),
            }

        await preferences_service.save_preferences(
            user_id=user_id,
            preferences=preferences
        )

        return {
            "extract_preference": False
        }

    return save_preferences_node