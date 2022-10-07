---
layout: default
title: Git
parent: Command Line Interface
permalink: /cli/git
---

# Git
> [Git](https://www.git-scm.com/) is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency. 

I'm mostly sure that most engineers and developers are using git right now, but
how well? Eh. Git is a massive and complex program that you don't get good at
overnight. And even if you git good, you might forget stuff. I forget stuff all
the time, so I have a doc here to help me remember all the little things.

## Ignore everything except a few files
Thanks to [this stackoverflow thread](https://stackoverflow.com/q/987142).

An optional prefix ! which negates the pattern; any matching file excluded by a previous pattern will become included again. If a negated pattern matches, this will override lower precedence patterns sources.

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

Thank you to [probable robot](https://probablerobot.net/2021/05/keeping-'live'-dotfiles-in-a-git-repo/) for this.
