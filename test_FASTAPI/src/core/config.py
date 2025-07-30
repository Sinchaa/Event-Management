import os
import urllib.parse
from os import listdir

# Initialize secrets dictionary
secrets = {}

# Use ENV from environment variable, default to 'local'
env = os.environ.get('ENV', 'local')

# Define path for secrets based on environment
pathRef = 'C:/Users/SINCHAS/Documents/etc/secrets'

# Read all secret files into the secrets dictionary
# try:
#     onlyfiles = [f for f in listdir(pathRef)]
#     for file in onlyfiles:
#         sfile_path = os.path.join(pathRef, file)
#         if os.path.isfile(sfile_path):
#             try:
#                 with open(sfile_path, "r") as f:
#                     file_content = f.read().strip()
#                     secrets[file] = file_content
#             except Exception as e:
#                 print(f"[ERROR] Could not read file {sfile_path}: {e}")
# except Exception as e:
#     print(f"[ERROR] Failed to list or read secrets from {pathRef}: {e}")


class Settings:
    PROJECT_NAME: str = "Mini Event Management System"
    PROJECT_VERSION: str = "1.0.0"

    ENV: str = env
    POSTGRES_USER = secrets.get('DBUSER', 'postgres')
    POSTGRES_PASSWORD = urllib.parse.quote(secrets.get(
        'DBPWD', 'root')).replace('%', '%%')
    POSTGRES_SERVER = secrets.get('DBHOST', 'localhost')
    POSTGRES_PORT = secrets.get('PORT', '5432')
    POSTGRES_DB = secrets.get('DBNAME', 'postgres')

    UC4_BATCH_RUN = secrets.get('X_API_KEY', '')

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SCHEMA: str = 'eprov'


settings = Settings()
