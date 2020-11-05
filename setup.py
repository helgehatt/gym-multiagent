from setuptools import setup, find_packages

setup(
    name="gym_multiagent",
    version="1.0.0",
    license="MIT",
    description="Sokoban-inspired multi-agent environment for OpenAI Gym",
    author="helgehatt",
    url="https://github.com/helgehatt/gym-multiagent",
    keywords=["multiagent", "openai", "gym", "environment"],
    install_requires=["gym", "numpy"],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
