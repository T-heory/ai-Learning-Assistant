import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, select
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class StudentRecord(Base):
    __tablename__ = "students"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    profile_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LearningProgress(Base):
    __tablename__ = "learning_progress"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    topic: Mapped[str] = mapped_column(String(256))
    path_json: Mapped[str] = mapped_column(Text, default="{}")
    current_step: Mapped[int] = mapped_column(default=0)
    completed: Mapped[str] = mapped_column(Text, default="[]")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExerciseRecord(Base):
    __tablename__ = "exercise_records"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    topic: Mapped[str] = mapped_column(String(256))
    question: Mapped[str] = mapped_column(Text)
    user_answer: Mapped[str] = mapped_column(Text)
    correct_answer: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_profile(session_id: str) -> dict:
    async with async_session() as session:
        result = await session.execute(
            select(StudentRecord).where(StudentRecord.id == session_id)
        )
        record = result.scalar_one_or_none()
        if record:
            return json.loads(record.profile_json)
        return {}


async def save_profile(session_id: str, profile: dict):
    async with async_session() as session:
        result = await session.execute(
            select(StudentRecord).where(StudentRecord.id == session_id)
        )
        record = result.scalar_one_or_none()
        if record:
            record.profile_json = json.dumps(profile, ensure_ascii=False)
            record.updated_at = datetime.utcnow()
        else:
            session.add(StudentRecord(
                id=session_id,
                profile_json=json.dumps(profile, ensure_ascii=False)
            ))
        await session.commit()
