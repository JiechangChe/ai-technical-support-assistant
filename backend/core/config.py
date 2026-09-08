from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int

    # LLM
    siliconflow_api_key: str
    llm_model: str = "deepseek-ai/DeepSeek-V3.2"
    llm_base_url: str = "https://api.siliconflow.cn/v1"

    # Embedding
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    #Reranker
    reranker_model: str = "BAAI/bge-reranker-base"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"localhost:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()