import argparse
import os
import subprocess

from src.core.config import Settings


if __name__ == "__main__":
    current_env = Settings.ENV
    environment = current_env if current_env else 'development'
    parser = argparse.ArgumentParser(
        description="Run FastAPI server with environment selection")
    parser.add_argument("--env", type=str,
                        default=environment, help="Environment to use")
    args, remaining_args = parser.parse_known_args()

    uvicorn_command = ["uvicorn", "src.main:app", "--host",
                       "0.0.0.0", "--port", "8000", "--reload", *remaining_args]

    try:

        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Alembic command executed successfully!")
            print(f"{result.stdout}")
        else:
            print("Alembic command failed!")
            print(f"{result.stderr}")
            exit(1)
        subprocess.run(uvicorn_command, check=True)

    except KeyboardInterrupt:
        print("Server stopped.")
