from setuptools import setup, find_packages

setup(
    name="backend",
    packages=find_packages(),
    version="0.1.0",
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "python-dotenv",
        "alembic",
        "pydantic[email]"
    ],
) 