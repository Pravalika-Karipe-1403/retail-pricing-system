import os
import subprocess

from config import get_settings


def generate_models_from_db():
    """
    Utility function to generate SQLAlchemy models from an existing database.
    Run this manually when you need to update models from the database.
    """
    settings = get_settings()

    # Create the output directory if it doesn’t exist
    os.makedirs("app/db", exist_ok=True)

    # Build the command
    # 1)To generate all the tables.
    cmd = (
        f"python -m sqlacodegen mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_SERVER}:{settings.MYSQL_PORT}/{settings.MYSQL_SCHEMA} --outfile app/db/retail_db_entities.py"
    )

    # Execute the command
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("Models generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error generating models: {e}")


if __name__ == "__main__":
    # This can be run as a standalone script
    generate_models_from_db()
