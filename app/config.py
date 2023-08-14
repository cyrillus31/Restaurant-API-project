from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    redis_host: str
    redis_port: str
    rabbit_host: str
    rabbit_port: str

    class Config:
        env_file = '.env'


settings = Settings()
