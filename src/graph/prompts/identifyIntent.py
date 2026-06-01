from pydantic import BaseModel
from typing import Optional, List, Literal
import json
from datetime import datetime

class JobIntentSchema(BaseModel):

    intent: Literal[
        "search_jobs",
        "unknown"
    ]

    role: Optional[str] = None
    location: Optional[str] = None
    seniority: Optional[str] = None
    company: Optional[str] = None
    remote: Optional[bool] = None


def get_system_prompt(companies):

    return json.dumps({

        "role": "Job Search Intent Classifier",

        "task": (
            "Identify if the user wants to search for jobs "
            "and extract all relevant filters"
        ),

        "available_companies": companies,

        "current_date": datetime.utcnow().isoformat(),

        "rules": {

            "search_jobs": {

                "description": (
                    "User wants to find job opportunities"
                ),

                "keywords": [
                    "vaga",
                    "job",
                    "posição",
                    "opportunity",
                    "trabalho",
                    "cientista de dados",
                    "engenheiro de ml",
                    "apply"
                ],

                "required_fields": [
                    "role"
                ],

                "optional_fields": [
                    "location",
                    "seniority",
                    "company",
                    "remote"
                ]
            },

            "unknown": {

                "description": (
                    "Anything unrelated to job searching"
                )
            }
        },

        "extraction_instructions": {

            "role": (
                "Extract the desired role exactly as "
                "mentioned by the user"
            ),

            "location": (
                "Extract preferred job location if mentioned"
            ),

            "seniority": (
                "Extract seniority level like "
                "junior, pleno, senior"
            ),

            "company": (
                "Match company names with available_companies"
            ),

            "remote": (
                "Detect whether the user wants "
                "remote work"
            )
        },

        "examples": [

            {

                "input": (
                    "Quero vagas de cientista de dados senior remoto"
                ),

                "output": {

                    "intent": "search_jobs",

                    "role": "cientista de dados",

                    "seniority": "senior",

                    "remote": True
                }
            },

            {

                "input": (
                    "Tem vaga de ML Engineer na Nubank?"
                ),

                "output": {

                    "intent": "search_jobs",

                    "role": "ML Engineer",

                    "company": "nubank"
                }
            },

            {

                "input": (
                    "Qual a previsão do tempo hoje?"
                ),

                "output": {

                    "intent": "unknown"
                }
            }
        ]

    }, indent=2)


def get_user_prompt(question):

    return json.dumps({

        "question": question,

        "instructions": [

            "Analyze the user request carefully",

            "Identify whether the user is searching for jobs",

            "Extract all relevant filters",

            "Return only fields explicitly mentioned",

            "Return valid JSON only"
        ]

    }, indent=2)