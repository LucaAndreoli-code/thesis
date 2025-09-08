import os
from dotenv import load_dotenv
import sys

if 'pytest' in sys.modules or 'pytest' in ' '.join(sys.argv) or 'test' in sys.argv:
    print("Loading TEST environment variables...")
    load_dotenv('.env.test', override=True)
else:
    print("Loading DEFAULT environment variables...")
    load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY")
