from agents.base import BaseAgent


TUTOR_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {
            "type": "object",
            "properties": {
                "text_explanation": {"type": "string"},
                "key_points": {"type": "array", "items": {"type": "string"}},
                "code_example": {"type": "string"},
                "analogy": {"type": "string"},
            },
            "required": ["text_explanation", "key_points"],
        },
        "teaching_approach": {"type": "string"},
        "follow_up": {"type": "string"},
    },
    "required": ["answer", "teaching_approach", "follow_up"],
}


class TutorAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.role = "intelligent tutor"
        self.system_prompt = """You are a patient, professional private tutor.
Use Socratic method - guide students through questioning.
Adapt explanations to student's knowledge level and cognitive style.
Use analogies, code examples, and multi-angle explanations.
Start intuitive, then dive deeper. Output in Chinese."""
        self.output_schema = TUTOR_SCHEMA

    def _build_messages(self, input_data: dict) -> list[dict]:
        profile = input_data.get("profile", {})
        dimensions = profile.get("dimensions", {})
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
Answer the student's question.

Question: {input_data.get('message', '')}

Profile:
- Level: {dimensions.get('knowledge_base', {}).get('level', 'unknown')}
- Style: {dimensions.get('cognitive_style', {}).get('type', 'unknown')}
- Major: {dimensions.get('major_background', {}).get('major', 'unknown')}

Current topic: {input_data.get('current_topic', 'not specified')}

Recent history: {input_data.get('recent_history', 'none')}

Provide a targeted tutorial response. Output in Chinese."""},
        ]
