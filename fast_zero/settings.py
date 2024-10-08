from pydantic_settings import BaseSettings, SettingsConfigDict


# o extra = ignore, permite que seja declaradas mais
# variaveis, mesmo que não utilizadas
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
