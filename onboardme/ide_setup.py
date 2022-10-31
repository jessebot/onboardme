 #!/usr/bin/env python3.10
 """
 NAME:    Onboardme.vim_neovim_setup
 DESC:    install vim and neovim
 AUTHOR:  Jesse Hitch
 LICENSE: GNU AFFERO GENERAL PUBLIC LICENSE
 """
 
 from os import path
 from pathlib import Path
 
 # rich helps pretty print everything
 from rich import print
 import wget
 
 # custom libs
 from .console_logging import print_panel, print_header, print_msg
 from .subproc import subproc
 
 
 # user env info
 PWD = path.dirname(__file__)
 
 
 def vim_setup():
     """
     Installs vim-plug: does a wget on plug.vim
     Installs vim plugins: calls vim with +PlugInstall/Upgrade/Upgrade
     Returns True
     """
     print_header('[b]vim-plug[/b] and [green][i]Vim[/i][/green] plugins '
                  'installation [dim]and[/dim] upgrades')
 
     # trick to not run youcompleteme init every single time
     init_ycm = False
     if not path.exists(f'{HOME_DIR}/.vim/plugged/YouCompleteMe/install.py'):
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
     subproc(['vim +PlugInstall +PlugUpgrade +PlugUpdate +qall!'], False, True)
     print_msg('[i][dim]Plugins installed.')
 
     if init_ycm:
         # This is for you complete me, which is a python completion module
         subproc(f'{HOME_DIR}/.vim/plugged/YouCompleteMe/install.py')
 
     return True
 
 
 def neovim_setup():
     """
     neovim plugins have a different setup path entirely:
     git clone --depth 1 https://github.com/wbthomason/packer.nvim  \
             {HOME_DIR}/.local/share/nvim/site/pack/packer/start/packer.nvim
     """
     local_share = ".local/share/nvim/site/pack/packer/start/packer.nvim"
     packer_dir = os.path.join(HOME_DIR, local_share)
 
     if not os.path.exists(packer_dir):
         cmd = 'git clone --depth 1 https://github.com/wbthomason/packer.nvim '
         cmd += packer_dir
         subproc([cmd])
 
     # installs the vim plugins if not installed, updates vim-plug, and then
     # updates all currently installed plugins
     subproc(['nvim +PackerInstall +PackerCompile +PlugUpdate +qall!'], False,
             True)
     print_msg('[i][dim]Plugins installed.')
 
     return True
