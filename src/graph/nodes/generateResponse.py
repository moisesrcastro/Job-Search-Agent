from langchain_core.messages import AIMessage

from src.config import model_config
from src.services.openRouter import OpenRouterService


NO_ROLE_SYSTEM_PROMPT = """
You are a friendly job search assistant.
"""

NO_ROLE_USER_PROMPT = """
The user has not specified which role they are looking for.

Ask naturally about:
- desired job title
- area of interest

Be concise, conversational, and helpful.
"""


NO_JOBS_SYSTEM_PROMPT = """
You are a professional recruitment assistant.
"""

NO_JOBS_USER_PROMPT = """
The user searched for the following role:

Role: {role}

No jobs were found.

Generate a natural response that:
- explains that no jobs were found
- suggests adjusting the search terms
- suggests related roles
- asks a follow-up question

Keep the tone friendly and conversational.
"""


JOBS_FOUND_SYSTEM_PROMPT = """
You are a professional job search assistant.
"""

JOBS_FOUND_USER_PROMPT = """
The user searched for:

Role: {role}

Jobs found:

{jobs}

Generate a natural response that:
- summarizes the opportunities
- highlights companies and positions
- provides context instead of simply listing jobs
- sounds conversational and helpful

Do not invent information.
"""


async def generate_response(state):

    jobs = state.get("jobs", [])
    role = state.get("role")

    service = OpenRouterService(model_config)

    if not role:

        result = await service.generate(
            system_prompt=NO_ROLE_SYSTEM_PROMPT,
            user_prompt=NO_ROLE_USER_PROMPT
        )

        return {
            "messages": [
                AIMessage(
                    content=(
                        result["text"]
                        if result["success"]
                        else "What kind of role are you looking for?"
                    )
                )
            ]
        }

    if not jobs:

        result = await service.generate(
            system_prompt=NO_JOBS_SYSTEM_PROMPT,
            user_prompt=NO_JOBS_USER_PROMPT.format(
                role=role
            )
        )

        return {
            "messages": [
                AIMessage(
                    content=(
                        result["text"]
                        if result["success"]
                        else f"I couldn't find any jobs for {role}. Would you like to try a different role?"
                    )
                )
            ]
        }

    result = await service.generate(
        system_prompt=JOBS_FOUND_SYSTEM_PROMPT,
        user_prompt=JOBS_FOUND_USER_PROMPT.format(
            role=role,
            jobs=jobs
        )
    )

    fallback = "\n".join(
        f"{job['title']} - {job['company']}"
        for job in jobs
    )

    return {
        "messages": [
            AIMessage(
                content=(
                    result["text"]
                    if result["success"]
                    else fallback
                )
            )
        ]
    }