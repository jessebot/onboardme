" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"                          @jessebot's personal .vimrc
" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                 GENERAL
"            stuff like line numbers and syntax highlighting
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Use 24-bit (true-color) mode in Neovim 0.1.5+ and Vim 7.4+
if (has("termguicolors"))
    set termguicolors
endif

" setting default colorscheme
set background=dark

" NERD FONTS - fonts with free glyphs require utf-8
set encoding=utf-8
" use specific font with the glyphs patched in
set guifont=Hack\ Nerd\ Font:h15

" line numbers for debugging and screen sharing
set number

" highlight current line - very useful, shouldn't turn off, you will be lost
set cursorline

" fix window to be 80 characters at start
set winwidth=80

" Enable syntax highlighting by default
syntax on

" remember more commands and search history
set history=10000

" allow backspacing over everything in insert mode
set backspace=indent,eol,start


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                            GENERAL - Part 2
"                     stuff I need to research more
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" allow unsaved background buffers and remember marks/undo for them
set hidden
set scrolloff=3
" Prevent Vim from clobbering the scrollback buffer. See
" http://www.shallowsky.com/linux/noaltscreen.html
set t_ti= t_te=

" This makes RVM work inside Vim. I have no idea why. ? RVM?
set shell=bash

" Store temporary files in a central spot ?
set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp

" display incomplete commands ?
set showcmd

" use emacs-style tab completion when selecting files, etc ?
set wildmode=longest,list
" make tab completion for files/buffers act like bash ?
set wildmenu

" https://medium.com/usevim/vim-101-what-is-the-leader-key-f2f5c1fa610f
" The <Leader> key is a reference to a specific key defined by the mapleader
" variable. A lot of ppl change to comma because they find it easier to type.
"
let mapleader=","

" unsure what this does and afraid to remove it...?
set nocompatible

" other stuff that I don't know if it matters...?
set cmdheight=2
set switchbuf=useopen
set numberwidth=5
set showtabline=2


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

" let spacebar take me into command mode
noremap <space> :

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
"                             <Leader>w
" Sudo vim trick with less key strokes - allow saving of files as sudo when I
"                      forgot to start vim using sudo.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
noremap <Leader>w :w !sudo tee % > /dev/null

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                              Airline
"               A pure vim script status line for vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" use powerline fonts
let g:airline_powerline_fonts = 1
" use softer colors
let g:airline_theme='murmur'
" changing separators to match personal powerline for shell
let g:airline_left_sep=' '
let g:airline_right_sep=''
" this is a smaller more consise final section
function! LinePercent()
    return line('.') * 100 / line('$') . '%'
endfunction
let g:airline_section_z = ':%l (%{LinePercent()}) :%v'


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               vim-gitgutter
"  git gutter is a vim plugin that puts a symbol in a column before the line #
"  We need to do a little configuring to make it less ugly
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" vim-gitgutter used to do this by default:
highlight! link SignColumn LineNr
" change sign color color
highlight SignColumn guibg=#1d1d1d ctermbg=black

" change the colors back to what they should be when there are changes
highlight GitGutterAdd    guifg=#009900 ctermfg=2
highlight GitGutterChange guifg=#bbbb00 ctermfg=3
highlight GitGutterDelete guifg=#ff2222 ctermfg=1

" use the nerdfont symbols inst4ead of -,+
let g:gitgutter_sign_added = ''
let g:gitgutter_sign_modified = ''
let g:gitgutter_sign_removed = ''


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                 Vim-plug
"         plugin manager for vim: https://github.com/junegunn/vim-plug
"          plugin directory will be (on Linux/macOS): '~/.vim/plugged'
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
call plug#begin()

" this is a modern fuzzy searcher
Plug 'liuchengxu/vim-clap'

" adds a pretty status line
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" git plugin for running git commands with :git
Plug 'tpope/vim-fugitive'
" puts a git + or - in side line to show git changes in file
Plug 'airblade/vim-gitgutter'

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

" indents lines and adds a line to show blocks of code
Plug 'Yggdroot/indentLine'

" yaml syntax highlighting better
Plug 'stephpy/vim-yaml'
" python tab completion - I actually find this kind of annoying :shrug:
Plug 'davidhalter/jedi-vim'
" I don't actually remember what this does...
Plug 'python-mode/python-mode', { 'for': 'python'}
" bash tab completion
Plug 'WolfgangMehner/bash-support'

" linter - will use shellcheck for bash and highlight broken code
Plug 'dense-analysis/ale'

" ------------------------- k8s -------------------------------
"
" For the current buffer (including modifications not on disk)
" :KubeApply :KubeDelete :KubeCreate
" And for the current directory (read from disk)
" :KubeApplyDir :KubeDeleteDir
Plug 'andrewstuart/vim-kubernetes'

" helm yaml specifically (includes go support) doesn't seem to work for
" auto-indenting, so it's off for now
" Plug 'towolf/vim-helm'

call plug#end()
