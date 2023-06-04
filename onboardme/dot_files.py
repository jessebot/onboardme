"""
This just handles keeping your home directory as a live git directory
"""
from itertools import zip_longest
from os import chdir, path
from pathlib import Path
# this is for rich text, to pretty print things
from rich import box
from rich.table import Table
# custom libs
from .constants import HOME_DIR, PWD, XDG_CONFIG_DIR
from .console_logging import print_panel, print_msg
from .subproc import subproc


xdg_git_config_dir = path.join(XDG_CONFIG_DIR, 'git')
Path(xdg_git_config_dir).mkdir(exist_ok=True)
XDG_GIT_CONFIG = path.join(xdg_git_config_dir, 'config')


def setup_dot_files(OS='Linux',
                    overwrite=False,
                    git_url="https://github.com/jessebot/dot_files.git",
                    branch="main",
                    dot_files_cfg_dir=f"{XDG_CONFIG_DIR}/dot_files") -> None:
    """
    note on how we're doing things, seperate dot files repo:
    https://probablerobot.net/2021/05/keeping-'live'-dotfiles-in-a-git-repo/


    """
    # create dot_files_cfg_dir if it doesn't exist/don't complain if it does
    # defaults to ~/.config/dot_files
    Path(dot_files_cfg_dir).mkdir(parents=True, exist_ok=True)
    chdir(dot_files_cfg_dir)
    opts = {'quiet': True, 'cwd': dot_files_cfg_dir}

    if git_url:
        if "github.com" in git_url:
            # get just the owner/repo_name like jessebot/dot_files
            user_repo = "/".join(git_url.split("/")[-2:]).replace(".git", "")

    # global: use main as default branch, always push up new remote branch
    git_raw = f"https://raw.githubusercontent.com/{user_repo}/{branch}"

    cmds = [f'curl {git_raw}/.config/git/config -o {XDG_GIT_CONFIG}',
            f'git --git-dir={dot_files_cfg_dir} --work-tree={HOME_DIR} init',
            'git config status.showUntrackedFiles no']
    subproc(cmds, spinner=False, **opts)

    # this one needs to be allowed to fail because it might already exist
    cmds = [f"git remote add origin {git_url}"]
    subproc(cmds, error_ok=True, spinner=False, **opts)

    # create ~/.config/.git to get git status while editing config files
    if not path.isfile(f"{XDG_CONFIG_DIR}/.git"):
        with open(f"{XDG_CONFIG_DIR}/.git", "w") as config_git_config:
            config_git_config.write(f"gitdir: {dot_files_cfg_dir}")

    if overwrite:
        # WARN: this command will overwrite local files with remote files
        reset_cmd = f"git reset --hard origin/{branch}"
    else:
        reset_cmd = f"git reset origin/{branch}"
        git_action = "[b]differ[/b] from"

    # fetch the latest changes, then reset to main, w/o overwriting anything
    subproc(['git fetch', reset_cmd], spinner=False, **opts)

    # get the latest remote modified and deleted files, if there are any
    git_files = subproc([f'git ls-files -m -d {HOME_DIR}'], **opts)

    if overwrite or not git_files:
        # if all the files are updated, just print them all as confirmation :)
        git_cmd = f"git ls-tree --full-tree -r --name-only origin/{branch}"
        git_files = subproc([git_cmd], spinner=False, **opts)
        git_action = "are up to date with"

    print_git_file_table(git_files, git_action, branch, git_url)
    chdir(PWD)

    if not overwrite and 'differ' in git_action:
        # we only print this msg if we got the file exists error
        msg = ("To [warn]:warning: overwrite[/warn] the existing dot files in "
               f"{HOME_DIR}/ with the file(s) listed in the above table, run:"
               "\n[green]onboardme [warn]--overwrite[/warn]")
        print_msg(msg)


def print_git_file_table(remote_git_files=[], file_verb="", branch="",
                         git_url="") -> None:
    """
    Takes a list of files and pretty prints them in a nice table in 2 columns:
        remote_git_files - [], list of files to print in 2 columns
        file_verb        - "", what is their relation to the origin/{branch}
        branch           - "", git branch we're looking at
        git_url          - "", url of git repo we're working with
    """
    emote = "[header]ʕ ･ᴥ･ʔ[/header][sky_blue1]"
    if "differ" in file_verb:
        emote = "[yellow]:warning: ʕ ⚈ᴥ⚈ʔ"
    # table to print the results of all the files
    table = Table(expand=True,
                  box=box.MINIMAL_DOUBLE_HEAD,
                  row_styles=["", "dim"],
                  border_style="dim",
                  show_header=False)
    table.add_column(" ", style="green")

    # remove all trailing space and then create a list of file paths
    # we make this a set to remove the duplicates
    files = set(remote_git_files.rstrip().replace("../..",
                                                  HOME_DIR).split('\n'))
    # then we make this a list so that zip_longest doesn't complain about sets
    f_list = list(files)
    if len(files) < 2:
        table.add_row(f_list[0])
    else:
        table.add_column(" ", style="green")

        # find midpoint of the list. if it's a float (e.g. 20.5) convert to int
        mid = int(len(files) / 2)
        # iterate over both halfs of list till the end of the longest list,
        for (f1, f2) in zip_longest(f_list[0:mid],
                                    f_list[mid:],
                                    fillvalue=" "):
            if f1 != " " and f2 != " ":
                table.add_row(f1, f2)
            else:
                table.add_row(f2, " ")

    git_repo = "[/grn]/[grn]".join(git_url.split('/')[-2:]).replace(".git", "")
    msg = (f"{emote} The following file(s) {file_verb} [grn]"
           f"origin[/grn]/[grn]{branch}[/grn] in [grn]{git_repo}")
    print_panel(table, msg, "left")
