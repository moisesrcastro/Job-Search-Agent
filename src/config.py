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


model_config = ModelConfigSchema(

    api_key=os.getenv("OPENROUTER_API_KEY", ""),

    http_referrer="engenharia-ia-aplicada.com",

    x_title="Job Finder AI",

    port=8000,

    models=[

        "google/gemma-3-27b-it",
        "meta-llama/llama-3.3-70b-instruct",
        "mistralai/mistral-small-3.1-24b-instruct"
    ],

    temperature=0.0,

    max_tokens=500,

    provider={
        "sort": "throughput"
    }
)