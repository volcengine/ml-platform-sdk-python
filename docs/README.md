# Write code doc in COMMENT!

Sphinx is a tool that makes it easy to create intelligent and beautiful documentation, which use the reStructuredText language to describe the generation content of docs.
The reStructuredText skeleton can automatically import packages and parse the docstring in installed source code. And finnal output format is set as `markdown`. You can refer to `./build/markdown/volcengine_ml_platform.io.md`

There are only one thing you need to care about: write correct comment in you source code


## Pre-require
install packages.
```shell
pip install -r dev-requirements.txt
```
## HOW to write docs

write docs in code with google style.

Request:
- write all of those in chinese. Of course, you can leave origin comment behind new comment.
- **must** comment in [google code style](https://google.github.io/styleguide/pyguide.html#:~:text=3.8%20Comments%20and%20Docstrings)
- The comment should follow the rule of reStructuredText, **markdown**. You can refer to `mlplatform-sdk-python/volcengine_ml_platform/io/tos.py`

## workflow example
```
write code and comment it
make update
make markdown
repeat util it completes
```

congratulations!
