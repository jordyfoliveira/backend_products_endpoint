from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int


settings = Settings()

#from pydantic_settings import BaseSettings, SettingsConfigDict


#class Settings(BaseSettings):
#    POSTGRES_HOST: str
#    POSTGRES_DB: str
#    POSTGRES_USER: str
#    POSTGRES_PASSWORD: str
#    POSTGRES_PORT: int

    #class Config:
    #    env_file = ".env"
    #    env_file_encoding = "utf-8"
    #model_config = SettingsConfigDict(
    #    env_file=".env",
    #    env_file_encoding="utf-8"
    #)


#settings = Settings()
#print(settings)