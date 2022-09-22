" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"                          @jessebot's personal .vimrc
" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                 GENERAL 
"              stuff like line numbers and syntax highlighting
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" NERD FONTS - fonts with free glyphs require utf-8 on & specific guifont var
set encoding=utf-8
set guifont=Hack\ Nerd\ Font:h15

" line numbers for debugging and screen sharing 
set number

" highlight current line - very useful, shouldn't turn off, you will be lost
set cursorline

" fix window to be 80 characters at start, I think
set winwidth=80

" Use 24-bit (true-color) mode in Neovim 0.1.5+ and Vim 7.4+
if (has("termguicolors"))
    set termguicolors
endif

" setting default colorscheme
set background=dark

" Enable syntax highlighting by default 
syntax on

" allow unsaved background buffers and remember marks/undo for them
set hidden

" remember more commands and search history
set history=10000

" unsure what this does and afraid to remove it...
set nocompatible


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                INDENT ZONE 
"                          define tabs and spaces
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
" Enable file type detection. Use the default filetype settings, so that mail
" gets 'tw' set to 72, 'cindent' is on in C files, etc.
" Also load indent files, to automatically do language-dependent indenting.
filetype plugin indent on


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                SEARCHING 
"                how we highlight search results and the like
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set laststatus=2
set showmatch
set incsearch
set hlsearch
" make searches case-sensitive only if they contain upper-case characters
set ignorecase smartcase
" solve issue where sometimes search is used with white text on yellow bg
hi Search ctermbg=White
hi Search ctermfg=DarkBlue

set cmdheight=2
set switchbuf=useopen
set numberwidth=5
set showtabline=2

" This makes RVM work inside Vim. I have no idea why.
set shell=bash

" Prevent Vim from clobbering the scrollback buffer. See
" http://www.shallowsky.com/linux/noaltscreen.html
set t_ti= t_te=
" keep more context when scrolling off the end of a buffer
set scrolloff=3
" Store temporary files in a central spot
set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
" allow backspacing over everything in insert mode
set backspace=indent,eol,start
" display incomplete commands
set showcmd
" use emacs-style tab completion when selecting files, etc
set wildmode=longest,list
" make tab completion for files/buffers act like bash
set wildmenu
let mapleader=","


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                            CUSTOM AUTOCMDS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
augroup vimrcEx
" Clear all autocmds in the group
  autocmd!
  autocmd FileType text setlocal textwidth=78
" Jump to last cursor position unless it's invalid or in an event handler
  autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \ exe "normal g`\"" |
    \ endif

" Leave the return key alone when in command line windows, since it's used
" to run commands there.
  autocmd! CmdwinEnter * :unmap <cr>
  autocmd! CmdwinLeave * :call MapCR()
augroup END


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                              MISC KEY MAPS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" not sure what this does :shrug:
map <leader>y "*y
" Move around splits with ctrl + nav key(hjkl)
nnoremap <c-j> <c-w>j
nnoremap <c-k> <c-w>k
nnoremap <c-h> <c-w>h
nnoremap <c-l> <c-w>l
" Clear the search buffer when hitting return
function! MapCR()
  nnoremap <cr> :nohlsearch<cr>
endfunction
call MapCR()
nnoremap <leader><leader> <c-^>


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                         MULTIPURPOSE TAB KEY
"     Indent if we're at the beginning of a line. Else, do completion.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! InsertTabWrapper()
    let col = col('.') - 1
    if !col || getline('.')[col - 1] !~ '\k'
        return "\<tab>"
    else
        return "\<c-p>"
    endif
endfunction
inoremap <tab> <c-r>=InsertTabWrapper()<cr>
inoremap <s-tab> <c-n>


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                    ARROW KEYS ARE UNACCEPTABLE :P
"              (really though, you should learn hjkl for vi)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <Left> <Nop>
map <Right> <Nop>
map <Up> <Nop>
map <Down> <Nop>


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                  OPEN FILES IN DIRECTORY OF CURRENT FILE
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
cnoremap %% <C-R>=expand('%:h').'/'<cr>
map <leader>e :edit %%
map <leader>v :view %%


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                            RENAME CURRENT FILE
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! RenameFile()
    let old_name = expand('%')
    let new_name = input('New file name: ', expand('%'), 'file')
    if new_name != '' && new_name != old_name
        exec ':saveas ' . new_name
        exec ':silent !rm ' . old_name
        redraw!
    endif
endfunction
map <leader>n :call RenameFile()<cr>


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               Md5 COMMAND
"                   Show the MD5 of the current buffer
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
command! -range Md5 :echo system('echo '.shellescape(join(getline(<line1>, <line2>), '\n')) . '| md5')


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                          OpenChangedFiles COMMAND
"                  Open a split for each dirty file in git
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! OpenChangedFiles()
  only " Close all windows, unless they're modified
  let status = system('git status -s | grep "^ \?\(M\|A\|UU\)" | sed "s/^.\{3\}//"')
  let filenames = split(status, "\n")
  exec "edit " . filenames[0]
  for filename in filenames[1:]
    exec "sp " . filename
  endfor
endfunction
command! OpenChangedFiles :call OpenChangedFiles()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                         InsertTime COMMAND 
"                       Insert the current time
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
command! InsertTime :normal a<c-r>=strftime('%F %H:%M:%S.0 %z')<cr>


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                    :w!!
" Sudo vim trick with less key strokes - allow saving of files as sudo when I
"                      forgot to start vim using sudo. 
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
cmap w!! w !sudo tee > /dev/null %

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               YAML
"                does proper linting w/o leaving vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab
  set foldlevelstart=20

  let g:ale_echo_msg_format = '[%linter%] %s [%severity%]'
  let g:ale_sign_error = '✘'
  let g:ale_sign_warning = '⚠'
  let g:ale_lint_on_text_changed = 'never'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                 Vim-plug
"         plugin manager for vim: https://github.com/junegunn/vim-plug
"          plugin directory will be (on Linux/macOS): '~/.vim/plugged'
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
call plug#begin()

" adds a pretty status line that uses powerline, might try airline as well...
Plug 'powerline/powerline'

" git plugin for running git commands with :git
Plug 'tpope/vim-fugitive'

" indents lines and adds a line to show blocks of code
Plug 'Yggdroot/indentLine'

" NerdTree - Tree explorer plugin - use :NERDTreeToggle to try it out
"          - after nerdtree is on visible, use ? for help
"
" On-demand loading of nerdtree
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
" syntax highlighing for nerdtree
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
" puts little glyphs for different file types
Plug 'ryanoasis/vim-devicons'
" add git awareness to see modified, merged, etc status of file in nerdtree
Plug 'Xuyuanp/nerdtree-git-plugin'
"
" END NerdTree

" this is a modern fuzzy searcher
Plug 'liuchengxu/vim-clap'

" yaml syntax highlighting better
" Plug 'stephpy/vim-yaml'
" helm yaml specifically (includes go support)
Plug 'towolf/vim-helm'

" python tab completion - I actually find this kind of annoying :shrug:
Plug 'davidhalter/jedi-vim'
" I don't actually remember what this does...
Plug 'python-mode/python-mode', { 'for': 'python', 'branch': 'develop' }
" bash tab completion
Plug 'WolfgangMehner/bash-support'

" linter - will use shellcheck for bash and highlight broken code
Plug 'dense-analysis/ale'

call plug#end()


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               STATUS LINE
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Powerline needs to be loaded last. Learn more about powerline here:
" https://powerline.readthedocs.io/en/master/usage/other.html#vim-statusline
python3 from powerline.vim import setup as powerline_setup
python3 powerline_setup()
python3 del powerline_setup

" Backup status line: left : filename, program, if the file has been modified
"                     right: line, coloumn
" :set statusline=%<%f\ (%{&ft})\ %-4(%m%)%=%-19(%3l,%02c%03V%)
