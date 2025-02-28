import asyncio

from src import app
from src.routes import *

if __name__ == '__main__':
    asyncio.run(app.serve())
