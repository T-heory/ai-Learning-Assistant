from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProfileDimension(BaseModel):
    level: str = Field(description="beginner/intermediate/advanced")
    description: str = Field(description="description")
    evidence: list[str] = Field(default_factory=list)


class StudentProfile(BaseModel):
    knowledge_base: ProfileDimension
    cognitive_style: ProfileDimension
    error_prone: ProfileDimension
    major_background: ProfileDimension
    learning_goal: ProfileDimension
    pace_preference: ProfileDimension


class Exercise(BaseModel):
    type: str = Field(description="choice/multi_choice/fill/code")
    difficulty: str = Field(description="easy/medium/hard")
    question: str
    options: Optional[list[str]] = Field(default=None)
    answer: str
    explanation: str


class Resource(BaseModel):
    document: str
    mindmap: str
    exercises: list[Exercise]
    readings: list[dict]
    practice: dict


class PathStep(BaseModel):
    day: int
    phase: str
    duration: str
    resources: list[str]
    description: str


class LearningPath(BaseModel):
    total_days: int
    steps: list[PathStep]
    prerequisites: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str
    session_id: str = Field(default="default")


class ChatResponse(BaseModel):
    reply: str
    profile_updated: bool = Field(default=False)


class AgentRequest(BaseModel):
    agent_type: str
    input_data: dict


class AgentResponse(BaseModel):
    agent_type: str
    output_data: dict


class GenerateResourcesRequest(BaseModel):
    topic: str
    session_id: str = Field(default="default")


class PlanPathRequest(BaseModel):
    topic: str
    session_id: str = Field(default="default")


class EvaluateRequest(BaseModel):
    session_id: str = Field(default="default")
    answers: list[dict] = Field(default_factory=list)
