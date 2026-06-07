from agents.base import BaseAgent


PATH_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "total_days": {"type": "integer"},
        "total_hours": {"type": "number"},
        "prerequisites": {"type": "array", "items": {"type": "string"}},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step": {"type": "integer"},
                    "phase": {"type": "string"},
                    "duration": {"type": "string"},
                    "objective": {"type": "string"},
                    "key_points": {"type": "array", "items": {"type": "string"}},
                    "resource_types": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"},
                },
                "required": ["step", "phase", "duration", "objective", "key_points", "description"],
            },
        },
        "tips": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "total_days", "total_hours", "steps", "tips"],
}


class PathPlannerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.role = "learning path planner"
        self.system_prompt = """You are a professional learning path planner.
Design scientific, personalized learning paths based on student profiles.
Progress from basics to advanced, align with cognitive patterns.
Each step should have clear objectives and recommended resource types. Output in Chinese."""
        self.output_schema = PATH_SCHEMA

    def _build_messages(self, input_data: dict) -> list[dict]:
        profile = input_data.get("profile", {})
        dimensions = profile.get("dimensions", {})
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
Design a learning path for:

Topic: {input_data.get('topic', '')}

Profile:
- Knowledge: {dimensions.get('knowledge_base', {}).get('level', 'unknown')}
- Pace: {dimensions.get('pace_preference', {}).get('speed', 'moderate')}
- Practice density: {dimensions.get('pace_preference', {}).get('practice_density', 'medium')}
- Goal: {dimensions.get('learning_goal', {}).get('short_term', '')}
- Long-term: {dimensions.get('learning_goal', {}).get('long_term', '')}

Completed: {input_data.get('completed_topics', 'none')}

Create a progressive learning path with clear scheduling. Output in Chinese."""},
        ]

    async def process(self, input_data: dict) -> dict:
        if "evaluation" in input_data:
            return await self._adjust_path(input_data)
        return await super().process(input_data)

    async def _adjust_path(self, input_data: dict) -> dict:
        messages = [
            {"role": "system", "content": "You are a learning path planner. Adjust learning plans based on evaluation results."},
            {"role": "user", "content": f"""
Current path: {input_data.get('current_path', {})}
Evaluation: {input_data.get('evaluation', {})}
Weaknesses: {input_data.get('weaknesses', [])}

Adjust the learning path to strengthen weak areas. Output in Chinese."""},
        ]
        result = await self.llm.chat_structured(messages, PATH_SCHEMA)
        return self._format_output(result, input_data)
