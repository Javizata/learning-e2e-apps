import asyncio
import selectors
import sys
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import URL, text


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env", env_file_encoding="utf-8")

    db_host: str
    db_port: int = Field(ge=1, le=65535)
    db_name: str
    db_user: str
    db_password: SecretStr


async def main() -> None:
    settings = Settings()

    url = URL.create(
        "postgresql+psycopg",
        username=settings.db_user,
        password=settings.db_password.get_secret_value(),
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )
    
    engine = create_async_engine(url)

    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text("SELECT current_user, current_database()")
            )
            user, database = result.one()
            print(f"Conexion correcta: usuario={user}, base={database}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.run(
            main(),
            loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()),
        )
    else:
        asyncio.run(main())