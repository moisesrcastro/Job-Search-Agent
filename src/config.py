import os

from dataclasses import dataclass
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ModelConfigSchema:

    api_key: str

    http_referrer: str

    x_title: str

    port: int

    models: List[str]

    temperature: float

    max_tokens: int

    provider: Dict[str, Any]


@dataclass
class DatabaseConfigSchema:

    host: str

    port: int

    database: str

    user: str

    password: str

    uri: str


@dataclass
class AppConfigSchema:

    max_messages_to_summary: int


model_config = ModelConfigSchema(

    api_key=os.getenv("OPENROUTER_API_KEY", ""),

    http_referrer="engenharia-ia-aplicada.com",

    x_title="Job Finder AI",

    port=8000,

    models=[
        "meta-llama/llama-3.3-70b-instruct"
    ],

    temperature=0.0,

    max_tokens=5000,

    provider={
        "sort": "throughput"
    }
)


database_config = DatabaseConfigSchema(

    host=os.getenv("POSTGRES_HOST", "localhost"),

    port=int(
        os.getenv(
            "POSTGRES_PORT",
            "5432"
        )
    ),

    database=os.getenv(
        "POSTGRES_DB",
        "jobfinder"
    ),

    user=os.getenv(
        "POSTGRES_USER",
        "postgres"
    ),

    password=os.getenv(
        "POSTGRES_PASSWORD",
        "postgres"
    ),

    uri=os.getenv(
        "POSTGRES_URI",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/jobfinder"
    )
)


app_config = AppConfigSchema(

    max_messages_to_summary=int(
        os.getenv(
            "MAX_MESSAGES_TO_SUMMARIZE",
            "6"
        )
    )
)