from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Vocal Assistance"
    bot_token: str 
    open_ai_token: str
    assistant_id: str

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding='utf-8')
