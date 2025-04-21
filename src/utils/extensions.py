from langchain_openai import ChatOpenAI

from src.adapters.postgres_adapter import PostgreSQL
from src.adapters.logger_adapter import LoggerAdapter
from src.utils.config import secrets


model = ChatOpenAI(api_key=secrets.get("OPENAI_API_KEY"))
postgres_instance = PostgreSQL()
logger = LoggerAdapter().get_logger()