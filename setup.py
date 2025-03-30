from setuptools import setup, find_packages

setup(
    name="journal_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.12.0",
        "newsapi-python>=0.2.7",
        "python-dotenv>=1.0.0",
        "schedule>=1.2.1",
        "jinja2>=3.1.3",
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "journal-ai=journal_ai.cli.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered newsletter system for Brazilian and international news",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/journal-ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 