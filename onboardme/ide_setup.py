"""
NAME:    Onboardme.ide_setup
DESC:    install vim, neovim, and fonts
AUTHORS:  Jesse Hitch, Max Roby
LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE
"""

import logging as log
from git import Repo, RemoteProgress
from os import path
from pathlib import Path

# custom libs
from .constants import HOME_DIR, OS
from .console_logging import print_header, print_sub_header, print_msg
from .subproc import subproc


def font_setup() -> None:
    """
    On Linux:
      Clones nerd-fonts repo and does a sparse checkout on only mononoki font.
      Also removes 70-no-bitmaps.conf and links 70-yes-bitmaps.conf

      Then runs install.sh from nerd-fonts repo
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
                    "git sparse-checkout add patched-fonts/VictorMono",
                    "git sparse-checkout add patched-fonts/NerdFontsSymbolsOnly",
                   ]
            subproc(cmds, spinner=True, cwd=fonts_dir)
        else:
            subproc(["git pull"], spinner=True, cwd=fonts_dir)

        subproc(['./install.sh Mononoki',
                 './install.sh VictorMono',
                 './install.sh NerdFontsSymbolsOnly'],
                quiet=True,
                cwd=fonts_dir)

        print_msg('[i][dim]The fonts should be installed, however, you have ' +
                  'to set your terminal font to the new font. I rebooted too.')


def neovim_setup() -> None:
    """
    Installs all plugins and syncs them if needed.
    Runs this command that works via the cli:
        nvim --headless "+Lazy! sync" +qa
    """
    print_header('[green][i]NeoVim[/i][/green] plugins installation '
                 '[dim]and[/dim] upgrades via [green]lazy.nvim[/green]')

    subproc(['nvim --headless ":Lazy sync" +qa',
             'nvim --headless ":TSUpdateSync" +qa'])

    print_sub_header('NeoVim Plugins installed.')
