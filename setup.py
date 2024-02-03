from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="py_spoo_url",
    version="0.0.6",
    description="Simple URL shortening with advanced analytics, emoji aliases, and more using spoo.me.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="https://github.com/spoo-me",
    author_email="support@spoo.me",
    url="https://github.com/spoo-me/py_spoo_url",
    license="MIT",
    packages=find_packages(),
    install_requires=["matplotlib", "requests", "geopandas", "pandas", "openpyxl"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
    ],
    project_urls={"spoo.me Service": "https://spoo.me"},
    keywords=[
        "URL shortening",
        "spoo.me",
        "URL analytics",
        "emoji aliases",
        "Python API",
        "custom aliasing",
        "password protection",
        "click tracking",
        "graph creation",
        "country heatmaps",
        "URL management",
        "Python package",
    ],
)
