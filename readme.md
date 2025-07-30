# About

This is a small collection of tutorials, which I use to understand core concepts of [Dagster](https://docs.dagster.io/). I share it as I use it as a reference but also learning resource.
Feel free to create a ticket, so that I can try to explain some concepts.

Each tutorial has its own `pyproject` configuration, so that you can run the projects individually. So you will find the code
for the components in the folder `/components`. 

Each project is initialized with `uvx -U create-dagster project <name>`, so I try to ensure that you can follow everything.

- I prefer to use `dagster-cli` instead of `dagster`. The difference is that i will rather use the `dg ...` command instead `dagster ...`.

# Run a test project
You do not need to do this but just checkout this repository, then run `uv sync` for each project you are interested in and that's it.
For example, you want to checkout the `components` project:

- `git clone git@github.com:azngeek/dagster-tutorials.git` (only once)
- `cd components`
- `uv sync`
- `dagster dev` or `dg dev` if you use the CLI.


# Content

- [Components](components.md)
