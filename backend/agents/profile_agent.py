import json
from agents.base import BaseAgent


PROFILE_SCHEMA = {
    "type": "object",
    "properties": {
        "dimensions": {
            "type": "object",
            "properties": {
                "knowledge_base": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "string", "enum": ["beginner", "intermediate", "advanced"]},
                        "description": {"type": "string"},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["level", "description", "evidence"],
                },
                "cognitive_style": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["visual", "verbal", "kinesthetic", "reading"]},
                        "description": {"type": "string"},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["type", "description", "evidence"],
                },
                "error_prone": {
                    "type": "object",
                    "properties": {
                        "categories": {"type": "array", "items": {"type": "string"}},
                        "description": {"type": "string"},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["categories", "description", "evidence"],
                },
                "major_background": {
                    "type": "object",
                    "properties": {
                        "major": {"type": "string"},
                        "year": {"type": "string"},
                        "related_skills": {"type": "array", "items": {"type": "string"}},
                        "description": {"type": "string"},
                    },
                    "required": ["major", "year", "related_skills", "description"],
                },
                "learning_goal": {
                    "type": "object",
                    "properties": {
                        "short_term": {"type": "string"},
                        "long_term": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["short_term", "long_term", "description"],
                },
                "pace_preference": {
                    "type": "object",
                    "properties": {
                        "speed": {"type": "string", "enum": ["slow", "moderate", "fast"]},
                        "practice_density": {"type": "string", "enum": ["low", "medium", "high"]},
                        "description": {"type": "string"},
                    },
                    "required": ["speed", "practice_density", "description"],
                },
            },
            "required": [
                "knowledge_base", "cognitive_style", "error_prone",
                "major_background", "learning_goal", "pace_preference"
            ],
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "summary": {"type": "string"},
    },
    "required": ["dimensions", "confidence", "summary"],
}


class ProfileAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.role = "student profile analyst"
        self.system_prompt = """You are an educational psychology expert and data analyst.
Your task is to build a six-dimension learning profile through conversation with students.
Analyze the student's dialogue to extract their learning characteristics across six dimensions:
knowledge base, cognitive style, error-prone areas, major background, learning goals, and pace preference.
Be objective and evidence-based. Output in Chinese."""
        self.output_schema = PROFILE_SCHEMA

    async def process(self, input_data: dict) -> dict:
        if "existing_profile" in input_data and input_data["existing_profile"]:
            return await self._incremental_update(input_data)
        return await super().process(input_data)

    async def _incremental_update(self, input_data: dict) -> dict:
        messages = [
            {"role": "system", "content": "You are an educational psychology expert. Based on existing profile and new dialogue, determine if profile needs updating. Return the complete updated profile."},
            {"role": "user", "content": f"""
Existing profile:
{input_data['existing_profile']}

New dialogue:
{input_data.get('message', '')}

Determine if profile update is needed and return the complete updated profile."""},
        ]
        result = await self.llm.chat_structured(messages, PROFILE_SCHEMA)
        return self._format_output(result, input_data)

    def _build_messages(self, input_data: dict) -> list[dict]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
Student dialogue:
{input_data.get('message', '')}

Analyze the above dialogue and build a six-dimension learning profile.
Return in specified JSON format."""},
        ]
