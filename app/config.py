from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    redis_host: str
    redis_port: int
    rabbit_host: str
    rabbit_port: int

    class Config:
        env_file = '.env'


settings = Settings()
