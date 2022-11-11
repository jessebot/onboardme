---
layout: default
title: Git
parent: Command Line Interface
permalink: /cli/git
---

# Git
> [Git][0] is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

I'm mostly sure that most engineers and developers are using git right now, but
how well? Eh. Git is a massive and complex program that you don't get good at
overnight. And even if you git good, you might forget stuff. I forget stuff all
the time, so I have a doc here to help me remember all the little things.

## precommit hooks with `pre-commit`
I recently learned about [pre-commit][1]. I found it when looking at [ruff][2]
to see if it made sense for pre-commit hooks.

```yaml
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.107
    hooks:
      - id: ruff
```

I also found that Poetry had [a page on pre-commit][3] as well. Example:

```yaml
hooks:
  - id: poetry-export
    args: ["-f", "requirements.txt"]
    verbose: true
```

## Ignore everything except a few files
Thanks to [this stackoverflow thread](https://stackoverflow.com/q/987142).

You can use an optional prefix of `!`, which negates the pattern; any matching
file excluded by a previous pattern will become included again. If a negated
pattern matches, this will override lower precedence patterns sources.

```gitignore
# Ignore everything
*

# But not these files...
!.gitignore
!script.pl
!template.latex
# etc...

# ...even if they are in subdirectories
!*/

# if the files to be tracked are in subdirectories
!*/a/b/file1.txt
!*/a/b/c/*
```

## Keeping all your dot files in a git repo

Thank you to [probable robot][4] for this.

## Deletion :warning:

### Deleting all commits before a certain date

Here's a couple of stackoverflow answers that were pretty helpful:

- [How can I delete all commits before a given date in Git history?][5]

- [How to delete the old git history][6]

### Remove file from git

[How Remove Files completely from git repository history][7]


[0]: https://www.git-scm.com/ "git-scm"
[1]: https://pre-commit.com/ "pre-commit"
[2]: https://github.com/charliermarsh/ruff "ruff"
[3]: https://python-poetry.org/docs/pre-commit-hooks/ "poetry pre-commit"
[4]: https://probablerobot.net/2021/05/keeping-'live'-dotfiles-in-a-git-repo/ "dotfiles git repo"
[5]: https://stackoverflow.com/q/29042783 "delete all commits before a date"
[6]: https://stackoverflow.com/questions/41953300/how-to-delete-the-old-git-history "delete old git history"
[7]: https://myopswork.com/how-remove-files-completely-from-git-repository-history-47ed3e0c4c35 "Remove Files completely from git"
