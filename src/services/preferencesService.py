from typing import Optional

from sqlalchemy import (
    String,
    Boolean,
    Text,
    DateTime,
    func,
    select
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from src.config import database_config

from datetime import datetime


class Base(DeclarativeBase):
    pass


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[str] = mapped_column(
        String,
        unique=True
    )

    role: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    location: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    seniority: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    company: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    remote: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True
    )

    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

class PreferencesService:

    def __init__(self):

        self.engine = create_async_engine(
            (
                f"postgresql+asyncpg://"
                f"{database_config.user}:"
                f"{database_config.password}@"
                f"{database_config.host}:"
                f"{database_config.port}/"
                f"{database_config.database}"
            ),
            echo=False
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def setup(self):

        async with self.engine.begin() as conn:

            await conn.run_sync(
                Base.metadata.create_all
            )

    async def get_preferences(
        self,
        user_id: str
    ) -> Optional[dict]:

        async with self.session_factory() as session:

            result = await session.execute(
                select(UserPreferences)
                .where(
                    UserPreferences.user_id == user_id
                )
            )

            preference = result.scalar_one_or_none()

            if not preference:
                return None

            return {
                "user_id": preference.user_id,
                "role": preference.role,
                "location": preference.location,
                "seniority": preference.seniority,
                "company": preference.company,
                "remote": preference.remote,
                "summary": preference.summary
            }

    async def save_preferences(
        self,
        user_id: str,
        preferences: dict
    ):

        async with self.session_factory() as session:

            result = await session.execute(
                select(UserPreferences)
                .where(
                    UserPreferences.user_id == user_id
                )
            )

            record = result.scalar_one_or_none()

            if not record:

                record = UserPreferences(
                    user_id=user_id
                )

                session.add(record)

            if preferences.get("role") is not None:
                record.role = preferences["role"]

            if preferences.get("location") is not None:
                record.location = preferences["location"]

            if preferences.get("seniority") is not None:
                record.seniority = preferences["seniority"]

            if preferences.get("company") is not None:
                record.company = preferences["company"]

            if preferences.get("remote") is not None:
                record.remote = preferences["remote"]

            await session.commit()

    async def save_summary(
        self,
        user_id: str,
        summary: str
    ):

        async with self.session_factory() as session:

            result = await session.execute(
                select(UserPreferences)
                .where(
                    UserPreferences.user_id == user_id
                )
            )

            record = result.scalar_one_or_none()

            if not record:

                record = UserPreferences(
                    user_id=user_id,
                    summary=summary
                )

                session.add(record)

            else:

                record.summary = summary

            await session.commit()

    async def get_summary(
        self,
        user_id: str
    ) -> Optional[str]:

        async with self.session_factory() as session:

            result = await session.execute(
                select(UserPreferences.summary)
                .where(
                    UserPreferences.user_id == user_id
                )
            )

            return result.scalar_one_or_none()

    async def get_basic_info(
        self,
        user_id: str
    ) -> Optional[str]:

        preferences = await self.get_preferences(
            user_id
        )

        if not preferences:
            return None

        parts = []

        if preferences.get("role"):
            parts.append(
                f"Preferred role: {preferences['role']}"
            )

        if preferences.get("location"):
            parts.append(
                f"Preferred location: {preferences['location']}"
            )

        if preferences.get("seniority"):
            parts.append(
                f"Seniority: {preferences['seniority']}"
            )

        if preferences.get("company"):
            parts.append(
                f"Preferred company: {preferences['company']}"
            )

        if preferences.get("remote") is not None:
            parts.append(
                f"Remote preference: {preferences['remote']}"
            )

        if preferences.get("summary"):
            parts.append(
                f"Conversation summary: {preferences['summary']}"
            )

        return "\n".join(parts) if parts else None

    async def close(self):

        await self.engine.dispose()