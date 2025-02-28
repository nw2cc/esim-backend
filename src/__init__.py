from amiyahttp import HttpServer, ServerConfig
from src.databases.user import get_user

app = HttpServer(
    host='0.0.0.0',
    port=32001,
    config=ServerConfig(get_user_password=get_user),
)
