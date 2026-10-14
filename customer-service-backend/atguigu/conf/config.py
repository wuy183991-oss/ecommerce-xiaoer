
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

#配置.env文件的实际路径
ENV_FILE = Path(__file__).parents[2] / ".env"

class Settings(BaseSettings):
    #LLM
    llm_model: str 
    llm_base_url: str
    llm_api_key: str

    #商城api
    commerce_api_base_url: str

    #数据库
    database_url: str 
    database_url_sync: str

    #服务器
    app_host: str
    app_port: int

    model_config = SettingsConfigDict(env_file=ENV_FILE,extra="ignore",env_file_encoding="utf-8")

#延迟加载
@lru_cache
def get_settings():
    print("初始化Settings")
    return Settings()

#预加载
settings = Settings()

if __name__ == "__main__":

    #读取预加载
    print(settings.llm_model)

    #读取延迟加载
    # settings =  get_settings()
    # print(settings.llm_model)