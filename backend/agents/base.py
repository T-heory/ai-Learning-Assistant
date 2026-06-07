import json
from abc import ABC, abstractmethod
from typing import Optional
from llm.deepseek_client import DeepSeekClient


class BaseAgent(ABC):
    def __init__(self, llm: DeepSeekClient):
        self.llm = llm
        self.role: str = ""
        self.system_prompt: str = ""
        self.output_schema: Optional[dict] = None

    async def process(self, input_data: dict) -> dict:
        messages = self._build_messages(input_data)
        if self.output_schema:
            result = await self.llm.chat_structured(messages, self.output_schema)
        else:
            text = await self.llm.chat(messages)
            result = {"content": text}
        return self._format_output(result, input_data)

    def _build_messages(self, input_data: dict) -> list[dict]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": json.dumps(input_data, ensure_ascii=False)},
        ]

    def _format_output(self, result: dict, input_data: dict) -> dict:
        return {
            "agent": self.role,
            "result": result,
            "input_summary": str(input_data.get("topic", input_data.get("message", "")))[:50],
        }
