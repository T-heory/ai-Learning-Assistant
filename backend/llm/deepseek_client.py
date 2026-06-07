import json
from typing import Optional
from openai import AsyncOpenAI
from config import settings


class DeepSeekClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )
        self.model = settings.DEEPSEEK_MODEL

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"[DeepSeek API Error] {e}")
            raise

    async def chat_stream(self, messages: list[dict], temperature: float = 0.7):
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"[DeepSeek Stream Error] {e}")
            yield f"\n\n[Error] {str(e)}"

    async def chat_structured(self, messages: list[dict], response_schema: dict, temperature: float = 0.3) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "structured_output",
                        "description": "Return result in structured format",
                        "parameters": response_schema,
                    },
                }],
                tool_choice={"type": "function", "function": {"name": "structured_output"}},
            )
            tool_call = response.choices[0].message.tool_calls[0]
            return json.loads(tool_call.function.arguments)
        except Exception as e:
            print(f"[DeepSeek Structured Error] {e}")
            raise
