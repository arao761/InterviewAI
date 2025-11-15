from setuptools import setup, find_packages

setup(
    name="prepwise-ai",
    version="0.1.0",
    description="AI/NLP intelligence layer for PrepWise interview preparation platform",
    author="PrepWise Team - Person 4 (AI/NLP Engineer)",
    author_email="team@prepwise.com",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "pypdf2>=3.0.0",
        "python-docx>=0.8.11",
        "pdfplumber>=0.10.0",
        "spacy>=3.7.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "tenacity>=8.2.0",
        "tiktoken>=0.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "ocr": [
            "pytesseract>=0.3.10",
        ],
        "vectordb": [
            "chromadb>=0.4.0",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
