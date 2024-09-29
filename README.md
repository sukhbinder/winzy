
[![PyPI](https://img.shields.io/pypi/v/winzy.svg)](https://pypi.org/project/winzy/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy/releases)
[![Tests](https://github.com/sukhbinder/winzy/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy/blob/main/LICENSE)


# winzy
A plugin-based CLI toolset for Windows, built on top of the Python language.

**Overview**
-----------

Winzy is a collection of command-line tools designed to make system administration and development tasks easier on Windows. The project takes a plugin-based approach, allowing users to extend its functionality by creating custom plugins.

**Features**
------------

*   A simple and intuitive CLI interface
*   Extensive plugin support for customizing and extending the toolset
*   Integration with popular Python libraries and frameworks
*   Support for multiple Python versions (>=3.9)

**Requirements**
----------------

*   Python 3.9 or later
*   The `pluggy` library for plugin management

**Installation**
----------------

```bash
pip install winzy
```

## Developing your plugin
------------------------

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed.

```bash
pipx install cookiecutter
```

Regular `pip` will work OK too.

## Usage

Run `cookiecutter gh:sukhbinder/winzy-plugin` and then answer the prompts. Here's an example run:

```bash
cookiecutter gh:sukhbinder/winzy-plugin
```

This will show this. Fill this and the template is ready. Just add your code.

```
plugin_name []: winzy plugin template demo
description []: Demonstrating https://github.com/sukhbinder/winzy-plugin
hyphenated [winzy-plugin-template-demo]:
underscored [winzy_plugin_template_demo]:
github_username []: sukhbinder
author_name []: Sukhbinder Singh
```


