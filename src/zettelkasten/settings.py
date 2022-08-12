from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 5000
    database_url: str = 'sqlite:///../db.sqlite'
    jwt_secret: str ='secret'
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    #ACCESS_TOKEN_EXPIRE_MINUTES = 30
    TEST_USERNAME = "username"
    TEST_USER_EMAIL = "test@example.com"
    TEST_PASSWORD = "password"




settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
