from openrouter import OpenRouter
from pydantic import BaseModel
from typing import Type, Optional
import asyncio


class OpenRouterService:

    def __init__(self, config):
        self.config = config

        self.client = OpenRouter(
            http_referer=self.config.http_referrer,
            x_open_router_title=self.config.x_title,
            api_key=self.config.api_key,
        )

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[BaseModel]
    ):
        try:

            def call_api():
                return self.client.chat.send(
                    model=self.config.models[0],
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": schema.__name__,
                            "schema": schema.model_json_schema()
                        }
                    },
                    temperature=self.config.temperature,
                    max_tokens=500
                )

            response = await asyncio.to_thread(call_api)

            content = response.choices[0].message.content
            parsed = schema.model_validate_json(content)

            return {
                "success": True,
                "data": parsed
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        try:

            def call_api():
                return self.client.chat.send(
                    model=self.config.models[0],
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature if temperature is not None else self.config.temperature,
                    max_tokens=max_tokens if max_tokens is not None else 500
                )

            response = await asyncio.to_thread(call_api)

            return {
                "success": True,
                "text": response.choices[0].message.content,
                "model": response.model
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }