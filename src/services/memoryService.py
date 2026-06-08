from dataclasses import dataclass

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

from src.config import database_config


@dataclass
class MemoryService:
    checkpointer: PostgresSaver
    store: PostgresStore


def create_memory_service() -> MemoryService:

    db_uri = (
        f"postgresql://"
        f"{database_config.user}:"
        f"{database_config.password}@"
        f"{database_config.host}:"
        f"{database_config.port}/"
        f"{database_config.database}"
    )

    store_cm = PostgresStore.from_conn_string(db_uri)
    store = store_cm.__enter__()

    checkpointer_cm = PostgresSaver.from_conn_string(db_uri)
    checkpointer = checkpointer_cm.__enter__()

    print("✅ Memory configured: PostgreSQL")

    return MemoryService(
        checkpointer=checkpointer,
        store=store
    )