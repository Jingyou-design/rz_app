from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    local_llm_api_key: str = Field(default="", validation_alias="LOCAL_LLM_API_KEY", description="本地模型 API 密钥")
    local_llm_base_url: str = Field(
        default="http://47.98.241.196:2224/v1",
        validation_alias="LOCAL_LLM_BASE_URL",
        description="本地模型 API 地址",
    )
    local_llm_model: str = Field(
        default="glm-5.3-flash",
        validation_alias="LOCAL_LLM_MODEL",
        description="本地模型名称",
    )
    local_llm_temperature: float = Field(
        default=0.0,
        validation_alias="LOCAL_LLM_TEMPERATURE",
        description="本地模型生成温度",
    )
settings = Settings()
