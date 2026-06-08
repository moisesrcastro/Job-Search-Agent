from src.services.getJobs import getJobs


COMPANIES = [
    "nubank",
    "spotify",
    "airbnb"
]


async def searchJobs(state):

    role = state.get("role")

    if not role:

        return {
            "jobs": [],
            "jobs_found": False,
            "should_search_jobs": False
        }

    jobs = await getJobs(
        role=role,
        COMPANIES=COMPANIES
    )

    print(jobs)

    return {
        "jobs": jobs,
        "jobs_found": len(jobs) > 0,
        "should_search_jobs": False
    }