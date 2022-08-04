from os import getenv


class Settings:
    DATABASE_NAME = getenv('POSTGRES_DB')
    DATABASE_USER = getenv('POSTGRES_USER')
    DATABASE_PASSWORD = getenv('POSTGRES_PASSWORD')
    DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}'


settings = Settings()
