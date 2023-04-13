import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] if os.environ["OPENAI_API_KEY"] else os.getenv("OPENAI_API_KEY", "")
print(f'OPENAI_API_KEY: {OPENAI_API_KEY}')

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
