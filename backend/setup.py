from setuptools import setup, find_packages

setup(
    name="video-downloader",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "yt-dlp",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
    ],
)