"""Этот модуль содержит конфигурацию базы данных для приложения.

Он включает настройку подключения к базе данных на основе переменных окружения.
"""

# THIRDPARTY
from pydantic import ConfigDict

# FIRSTPARTY
from app.database.db_base_config import Settings

ENV_FILENAME = '.prod.env'


class SettingsProdEnvironment(Settings):
    """Класс для настройки подключения к основной базе данных.

    Этот класс переопределяет переменные окружения, необходимые для
    подключения к основной базе данных.
    """

    model_config = ConfigDict(env_file=ENV_FILENAME)


settings = SettingsProdEnvironment()
engine = settings.get_engine()
session = settings.get_sessionmaker()
