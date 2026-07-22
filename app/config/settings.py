from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    deepseek_api_key: str = Field(default="", validation_alias="DEEPSEEK_API_KEY", description="DeepSeek API 密钥")
    deepseek_base_url: str = Field(
        default="https://api.deepseek.com/v1",
        validation_alias="DEEPSEEK_BASE_URL",
        description="DeepSeek API 地址",
    )
    deepseek_model: str = Field(
        default="deepseek-v4-flash",
        validation_alias="DEEPSEEK_MODEL",
        description="DeepSeek 模型名称",
    )
    deepseek_temperature: float = Field(
        default=0.0,
        validation_alias="DEEPSEEK_TEMPERATURE",
        description="DeepSeek 生成温度",
    )
settings = Settings()
