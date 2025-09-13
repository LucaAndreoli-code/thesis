import os
from dotenv import load_dotenv
import sys

if 'pytest' in sys.modules or 'pytest' in ' '.join(sys.argv) or 'test' in sys.argv:
    print("Loading TEST environment variables...")
    load_dotenv('.env.test', override=True)
else:
    print("Loading DEFAULT environment variables...")
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres")
SECRET_KEY = os.getenv("SECRET_KEY")
ROOT_PATH = os.getenv("ROOT_PATH", "")
