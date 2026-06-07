from agents.base import BaseAgent


EVAL_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_score": {"type": "number", "minimum": 0, "maximum": 100},
        "knowledge_mastery": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "score": {"type": "number"},
                    "level": {"type": "string", "enum": ["weak", "medium", "strong"]},
                    "suggestion": {"type": "string"},
                },
                "required": ["score", "level", "suggestion"],
            },
        },
        "weaknesses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "description": {"type": "string"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["topic", "description", "severity"],
            },
        },
        "strengths": {"type": "array", "items": {"type": "string"}},
        "learning_advice": {"type": "string"},
        "profile_updates": {
            "type": "object",
            "properties": {
                "error_prone_categories": {"type": "array", "items": {"type": "string"}},
                "knowledge_base_level": {"type": "string"},
            },
        },
    },
    "required": ["overall_score", "knowledge_mastery", "weaknesses", "strengths", "learning_advice"],
}


class EvaluatorAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.role = "learning evaluation analyst"
        self.system_prompt = """You are a professional learning evaluation analyst.
Evaluate student performance across multiple dimensions:
knowledge mastery, weaknesses, strengths, and progress.
Be objective, constructive, and encouraging. Output in Chinese."""
        self.output_schema = EVAL_SCHEMA

    def _build_messages(self, input_data: dict) -> list[dict]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
Evaluate the following learning data:

Topic: {input_data.get('topic', 'not specified')}
Answers: {input_data.get('answers', 'no data')}
Profile: {input_data.get('profile', 'none')}
Progress: {input_data.get('progress', 'just started')}

Assess learning effectiveness, identify weaknesses, give advice. Output in Chinese."""},
        ]
