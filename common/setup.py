from setuptools import setup, find_packages

setup(
    name="common",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.6.1",
        "python-dotenv>=1.0.1",
        "httpx>=0.26.0",
    ],
    author="MediaLab",
    description="Common library for MediaLab server and client",
    python_requires=">=3.11",
) 