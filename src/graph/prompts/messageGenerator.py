import json

def get_summary_prompt(role, jobs):

    return json.dumps({

        "role": "Job Recommendation Assistant",

        "task": (
            "Summarize the job opportunities "
            "returned by the API"
        ),

        "user_request": role,

        "jobs_found": len(jobs),

        "jobs": jobs,

        "instructions": [

            "If no jobs were found, say that clearly",

            "If jobs were found, summarize the best matches",

            "Mention company name, title and location",

            "Keep the answer concise",

            "Do not invent information"

        ]

    }, indent=2)