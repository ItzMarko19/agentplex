from setuptools import setup, find_packages

setup(
    name="agentplex",
    version="0.1.0",
    description="DAG-based multi-agent workflow engine",
    author="chu2bard",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0",
        "networkx>=3.0",
    ],
)
