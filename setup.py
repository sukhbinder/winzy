from setuptools import setup, find_packages

setup(
    name="winzy",
    version="0.0.1",
    description="CLI tools for windows. A plugin based approach.",
    packages=find_packages(),
    entry_points={"console_scripts": ["winzy = winzy.cli:main"]},
    install_requires =["pluggy",],
    python_requires=">=3.9",
    author="Sukhbinder Singh",
    url="https://github.com/sukhbinder/winzy",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],

    )
