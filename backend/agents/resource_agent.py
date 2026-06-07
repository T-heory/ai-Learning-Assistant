from agents.base import BaseAgent


RESOURCE_SCHEMA = {
    "type": "object",
    "properties": {
        "document": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string", "description": "Markdown formatted content"},
            },
            "required": ["title", "content"],
        },
        "mindmap": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "mermaid_code": {"type": "string", "description": "Mermaid.js syntax for mindmap, e.g. graph TD\\n  A[Center]\\n  A --> B[Sub1]"},
            },
            "required": ["title", "mermaid_code"],
        },
        "exercises": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["choice", "multi_choice", "fill", "code"]},
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
                    "question": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "answer": {"type": "string"},
                    "explanation": {"type": "string"},
                },
                "required": ["type", "difficulty", "question", "answer", "explanation"],
            },
        },
        "readings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["title", "summary", "reason"],
            },
        },
        "practice": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "steps": {"type": "array", "items": {"type": "string"}},
                "code": {"type": "string"},
                "expected_output": {"type": "string"},
            },
            "required": ["title", "description", "steps", "code", "expected_output"],
        },
    },
    "required": ["document", "mindmap", "exercises", "readings", "practice"],
}


class ResourceAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.role = "course content expert"
        self.system_prompt = """You are an experienced course content expert and instructional designer.
Generate personalized learning resources based on student profile and topic.
Adjust depth by knowledge level, adapt style by cognitive preference.
Generate all 5 resource types: document (Markdown), mindmap (Mermaid), exercises (3+ questions), readings (2-3), practice (with code). Output in Chinese."""
        self.output_schema = RESOURCE_SCHEMA

    def _build_messages(self, input_data: dict) -> list[dict]:
        profile = input_data.get("profile", {})
        dimensions = profile.get("dimensions", {})
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
Generate personalized learning resources for:

Topic: {input_data.get('topic', '')}

Student Profile:
- Knowledge: {dimensions.get('knowledge_base', {}).get('level', 'unknown')} - {dimensions.get('knowledge_base', {}).get('description', '')}
- Cognitive style: {dimensions.get('cognitive_style', {}).get('type', 'unknown')}
- Major: {dimensions.get('major_background', {}).get('major', 'unknown')}
- Goal: {dimensions.get('learning_goal', {}).get('short_term', '')}

Generate 5 resources: document, mindmap, exercises, readings, practice. Output in Chinese."""},
        ]
