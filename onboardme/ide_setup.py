#!/usr/bin/env python3.10
"""
NAME:    Onboardme.ide_setup
DESC:    install vim, neovim, and fonts
AUTHOR:  Jesse Hitch
LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE
"""

import logging as log
from git import Repo, RemoteProgress
from os import path
from pathlib import Path
import wget

# custom libs
from .console_logging import print_header, print_msg
from .subproc import subproc
from .env_config import HOME_DIR, OS


def vim_setup():
    """
    Installs vim-plug: does a wget on plug.vim
    Installs vim plugins: calls vim with +PlugInstall/Upgrade/Upgrade
    Returns True
    """
    print_header('[b]vim-plug[/b] and [green][i]Vim[/i][/green] plugins '
                 'installation [dim]and[/dim] upgrades')
    print('')

    # trick to not run youcompleteme init every single time
    init_ycm = False
    ycm_dir = path.join(HOME_DIR, '.vim/plugged/YouCompleteMe/install.sh')
    if not path.exists(ycm_dir):
        init_ycm = True

    # this is for installing vim-plug
    autoload_dir = f'{HOME_DIR}/.vim/autoload'
    url = 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    if not path.exists(autoload_dir):
        print_msg('[i]Creating directory structure and downloading [b]' +
                  'vim-plug[/b]...')
        Path(autoload_dir).mkdir(parents=True, exist_ok=True)
        wget.download(url, autoload_dir)

    # installs the vim plugins if not installed, updates vim-plug, and then
    # updates all currently installed plugins
    subproc(['vim +PlugInstall +PlugUpgrade +PlugUpdate +qall!'],
            quiet=True)
    print_msg('[i][dim]Vim Plugins installed.')

    if init_ycm:
        # This is for you complete me, which is a python completion module
        subproc(ycm_dir)

    return True


def neovim_setup():
    """
    neovim plugins have a setup mostly already handled in your plugins.lua:
    https://github.com/wbthomason/packer.nvim#bootstrapping
    This is the command that works via the cli:
    nvim --headless -c 'autocmd User PackerComplete quitall' -c 'PackerSync'

    uses special command (with packer bootstrapped) to have packer setup your
    your configuration (or simply run updates) and close once all operations
    are completed
    """
    print_header('[b]packer[/b] and [green][i]NeoVim[/i][/green] plugins '
                 'installation [dim]and[/dim] upgrades')
    print('')

    # updates all currently installed plugins
    commands = ["nvim --headless +PackerInstall",
                "nvim --headless +PackerSync"]
    subproc(commands)

    print_msg('[i][dim]NeoVim Plugins installed.')

    return True


def font_setup():
    """
    Clones nerd-fonts repo and does a sparse checkout on only mononoki and
    hack fonts. Also removes 70-no-bitmaps.conf and links 70-yes-bitmaps.conf

    Then runs install.sh from nerd-fonts repo

    ripped out of setup.sh recently:
        # we do this for Debian, to download custom fonts during onboardme
        if [[ "$OS" == *"Linux"* ]]; then
            mkdir -p ~/.local/share/fonts
        fi
    """
    if 'Linux' in OS:
        print_header('📝 [i]font[/i] installations')
        fonts_dir = f'{HOME_DIR}/repos/nerd-fonts'

        # do a shallow clone of the repo
        if not path.exists(fonts_dir):
            log.info('Nerdfonts require some setup on Linux...')
            bitmap_conf = '/etc/fonts/conf.d/70-no-bitmaps.conf'
            log.info(f'Going to remove {bitmap_conf} and link a yes map...')
            # we do all of this with subprocess because I want the sudo prompt
            if path.exists(bitmap_conf):
                subproc([f'sudo rm {bitmap_conf}'], quiet=True, spinner=False)

            cmd = ('sudo ln -s /etc/fonts/conf.avail/70-yes-bitmaps.conf '
                   '/etc/fonts/conf.d/70-yes-bitmaps.conf')
            subproc([cmd], error_ok=True, quiet=True, spinner=False)

            print_msg('[i]Downloading installer and font sets... ')

            Path(fonts_dir).mkdir(parents=True, exist_ok=True)
            fonts_repo = 'https://github.com/ryanoasis/nerd-fonts.git'

            class CloneProgress(RemoteProgress):
                def update(self, op_code, cur_count, max_count=None,
                           message=''):
                    if message:
                        log.info(message)

            Repo.clone_from(fonts_repo, fonts_dir, progress=CloneProgress(),
                            multi_options=['--sparse', '--filter=blob:none'])
            cmds = ["git sparse-checkout add patched-fonts/Mononoki",
                    "git sparse-checkout add patched-fonts/Hack"]
            subproc(cmds, spinner=True, cwd=fonts_dir)
        else:
            subproc(["git pull"], spinner=True, cwd=fonts_dir)

        subproc(['./install.sh Hack', './install.sh Mononoki'], quiet=True,
                cwd=fonts_dir)

        print_msg('[i][dim]The fonts should be installed, however, you have ' +
                  'to set your terminal font to the new font. I rebooted too.')
        return

    return
