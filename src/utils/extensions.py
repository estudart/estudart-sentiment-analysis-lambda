from adapters.postgres_adapter import PostgreSQL
from adapters.logger_adapter import LoggerAdapter

postgres_instance = PostgreSQL()
logger = LoggerAdapter().get_logger()