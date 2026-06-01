from src.services.openRouter import OpenRouterService
from src.config import model_config
from src.graph.prompts.identifyIntent import (
    JobIntentSchema,
    get_system_prompt,
    get_user_prompt
)

from src.graph.nodes.searchJobs import getJobs


async def search_jobs(state):

    COMPANIES = ["nubank", "spotify", "airbnb"]

    openrouter = OpenRouterService(model_config)

    result = await openrouter.generate_structured(
        system_prompt=get_system_prompt(COMPANIES),
        user_prompt=get_user_prompt(
            state["messages"][-1].content
        ),
        schema=JobIntentSchema
    )

    if not result["success"]:
        return {
            "jobs": [],
            "jobs_found": False,
            "role": None
        }

    structured = result["data"]

    role = structured.role
    
    if not role:
        return {
            "jobs":structured,
            "jobs_found": False,
            "role": None
        }

    jobs = await getJobs(
        role=role,
        COMPANIES=COMPANIES
    )

    return {
        "role": role,
        "jobs": jobs,
        "jobs_found": len(jobs) > 0
    }