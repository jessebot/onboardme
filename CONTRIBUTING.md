# Contributing
Always happy to review pull requests and merge any fixes, or features, that would help onboardme.

Here's some guidelines on how we code.

## Getting Started

<details>
  <summary><bold>Prereqs</bold><summary>

- Install [poetry], which we use for dependency management and packaging in python.

- If using vim/neovim, we recommend installing the [jedi language server]. onboardme will install it for you with the following:
```bash
# if you have existing dot files that you don't mind overwriting, use append -O
onboardme -s dot_files,neovim_setup --git_url https://github.com/jessebot/onboardme.git
```

</details>

Once you have the pre-reqs installed you can fork the [repo] and then clone your fork:

```bash
# this should be YOUR fork, but for an example, we're using the actual repo
git clone git@github.com:jessebot/onboardme.git
cd onboardme
```

Use `poetry` and `pre-commit` to install onboardme depedencies:
```bash
poetry install
pre-commit install
```

Now you can proceed as normal for python development and when you're done, just commit the changes and the pre-commit hooks will run any linting and tests we have. When everything passes, open up a PR against the main repo and we'll get it reviewed :)


[repo]: https://github.com/jessebot/onboardme/ "onboardme repo"
[pre-commit]: https://pre-commit.com/#install "pre-commit, for running actions before commits"
[poetry]: https://python-poetry.org/docs/#installation "poetry, tool for dependency management and packaging in Python"
[jedi language server]: https://github.com/pappasam/jedi-language-server#editor-setup
