import json

from pydantic import BaseModel
from typing import Optional


class SummarySchema(BaseModel):

    key_preferences: str

    important_context: Optional[str] = None
    
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

def get_summarization_system_prompt():

    return json.dumps({

        "role": (
            "Conversation summarizer for a job search assistant"
        ),

        "task": (
            "Analyze the conversation and maintain a "
            "structured summary of the user's job preferences"
        ),

        "fields_to_extract": {

            "desired_role":
                "Desired role or position",

            "preferred_location":
                "Preferred location",

            "preferred_seniority":
                "Desired seniority level",

            "preferred_companies":
                "Companies mentioned positively",

            "remote_preference":
                "Whether the user prefers remote work",

            "key_preferences":
                (
                    "2-4 sentence summary of the user's "
                    "career goals and preferences"
                ),

            "important_context":
                (
                    "Additional relevant professional context"
                )
        },

        "rules": [

            "Merge duplicated information",

            "Preserve information from previous summaries",

            "Only include information explicitly mentioned",

            "Do not invent preferences",

            "Update preferences when the user changes them"
        ]

    }, indent=2)

def get_summarization_user_prompt(
    conversation_history,
    previous_summary=None
):

    return json.dumps({

        "conversation": "\n".join(

            f"{msg['role']}: {msg['content']}"

            for msg in conversation_history

        ),

        "previous_summary": (
            previous_summary
            if previous_summary
            else "None"
        ),

        "instructions": [

            (
                "Update the summary using the "
                "new information from the conversation"
            ),

            (
                "Preserve previous information that "
                "was not contradicted"
            )

        ]

    }, indent=2)