" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"                       "vimrc of @jessebot on GitHub"
" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                 GENERAL:
"                    "line numbers, cursorline, etc,"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" line numbers for debugging and screen sharing
set number

" highlight current line - very useful, shouldn't turn off, you will be lost
set cursorline

" fix window to be 80 characters at start
set winwidth=80

" allow backspacing over everything in insert mode
set backspace=indent,eol,start

set shell=bash\ --login
" remember more commands and search history
set history=10000

let g:ycm_enable_semantic_highlighting=1

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                              MISC KEY MAPS:
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" for writing custom commands
" https://medium.com/usevim/vim-101-what-is-the-leader-key-f2f5c1fa610f
" The <Leader> key is a reference to a specific key defined by the mapleader
" variable. A lot of ppl change to comma because they find it easier to type.
let mapleader=","

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
"                         MULTIPURPOSE TAB KEY:
"     "Indent if we're at the beginning of a line. Else, do completion."
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
"              Disable arrow keys to force using vi navigation:
"              "(really though, you should learn hjkl for vi)"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <Left> <Nop>
map <Right> <Nop>
map <Up> <Nop>
map <Down> <Nop>

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                             Syntax And Colors:
"                  "Syntax highlighting and colorscheme"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Use 24-bit (true-color) mode in Neovim 0.1.5+ and Vim 7.4+
if (has("termguicolors"))
    set termguicolors
endif

" Enable syntax highlighting by default
syntax on
" gray line on the 80 character line, so you know when you're over 80 char
set colorcolumn=80
" custom colorscheme to be more pastel and pretty
colorscheme chalky

" clap
let g:clap_theme = 'material_design_dark'

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                Font Style:
"  "Using a fancy font if we have a gui, making sure we have utf-8 encoding"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" fonts with icons/emojis require utf-8
set encoding=utf-8
" use specific font with the glyphs patched in
set guifont=Mononoki\ Nerd\ Font:h15


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                           GENERAL Part Two:
"                     "stuff I need to research more"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" allow unsaved background buffers and remember marks/undo for them
set hidden
set scrolloff=3
" Prevent Vim from clobbering the scrollback buffer. See
" http://www.shallowsky.com/linux/noaltscreen.html
set t_ti= t_te=


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

" unsure what this does and afraid to remove it...?
set nocompatible

" other stuff that I don't know if it matters...?
set switchbuf=useopen
set numberwidth=5

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               FOLDING ZONE:
"                    "collapse an entire block or function"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Enable folding on base indent
set foldmethod=indent
set foldlevel=99
" let spacebar allow me to fold the code
nnoremap <space> za
" also allow me to see the doc strings
let g:SimpylFold_docstring_preview=1


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                INDENT ZONE:
"                          "define tabs and spaces"
"
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
" yaml needs a bit of help
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab foldlevelstart=20


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                               Ale:
"           "linter warning and errors using existing linters"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

let g:ale_echo_msg_format = '[%linter%] %s [%severity%]'
let g:ale_sign_error = '✘'
let g:ale_sign_warning = '⚠'
let g:ale_lint_on_text_changed = 'never'


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                SEARCHING:
"                "how we highlight search results and the like"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set laststatus=2
set showmatch
set incsearch
set hlsearch
" make searches case-sensitive only if they contain upper-case characters
set ignorecase smartcase
" solve issue where sometimes search is used with white text on yellow bg

" Make * search the file for text when you highlight it in visual mode
xnoremap * :<C-u>call <SID>VSetSearch()<CR>/<C-R>=@/<CR><CR>
xnoremap # :<C-u>call <SID>VSetSearch()<CR>?<C-R>=@/<CR><CR>

function! s:VSetSearch()
    let temp = @s
    norm! gv"sy
    let @/ = '\V' . substitute(escape(@s, '/\'), '\n', '\\n','g')
    let @s = temp
endfunction
" Above is from from this user: https://stackoverflow.com/a/42776237


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                            CUSTOM AUTOCMDS:
"
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
"                            CUSTOM Commands:
"                 "Locally defined commands for helpfulness"
"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


" remove trailing whitespaces
command! FixWhitespace :%s/\s\+$//e

" OPEN FILES IN DIRECTORY OF CURRENT FILE
map <leader>e :edit %%
map <leader>v :view %%


" RENAME CURRENT FILE
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

" Md5 COMMAND - Show the MD5 of the current buffer"
command! -range Md5 :echo system('echo '.shellescape(join(getline(<line1>, <line2>), '\n')) . '| md5')


" OpenChangedFiles - Open a split for each dirty file in git
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

" Insert the current time
command! InsertTime :normal a<c-r>=strftime('%F %H:%M:%S.0 %z')<cr>

" <Leader>w
" Sudo vim trick with less key strokes - allow saving of files as sudo when I
" forgot to start vim using sudo.
noremap <Leader>w :w !sudo tee % > /dev/null


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                              Airline:
"               "A pure vim script status line for vim"
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
"                               Gitgutter:
" "vim-gitgutter is a vim plugin that puts a symbol in a column to the left"
"  "We need to do a little configuring to make it less ugly"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" use the nerdfont symbols inst4ead of -,+
let g:gitgutter_sign_added = ''
let g:gitgutter_sign_modified = ''
let g:gitgutter_sign_removed = ''

" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"                                "vim-plug"
"         "plugin manager for vim: https://github.com/junegunn/vim-plug
"          plugin directory will be (on Linux/macOS): '~/.vim/plugged'
" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
call plug#begin()

" -------------------- General IDE stuff ------------------------
" adds a pretty status line
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
" allow collapsing of functions for python and other supported languages
Plug 'tmhedberg/SimpylFold'
" indents lines and adds a line to show blocks of code
Plug 'Yggdroot/indentLine'
" this is a modern fuzzy searcher
Plug 'liuchengxu/vim-clap'

" NerdTree - Tree explorer plugin - use :NERDTreeToggle to try it out
"          - after nerdtree is on visible, use ? for help
"
" On-demand loading of nerdtree
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
" add tabs to nerdtree - experimental
Plug 'jistr/vim-nerdtree-tabs'
" puts little glyphs for different file types
Plug 'ryanoasis/vim-devicons'
" syntax highlighing for nerdtree
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
" add git awareness to see modified, merged, etc status of file in nerdtree
Plug 'Xuyuanp/nerdtree-git-plugin'

" git plugin for running git commands with :git
Plug 'tpope/vim-fugitive'
" puts a git + or - in side line to show git changes in file
Plug 'airblade/vim-gitgutter'

" general linter - will use common linters and highlight broken code
Plug 'dense-analysis/ale'

" ---------- Language Specific/File type Specific Stuff -------------

" terraform linter
Plug 'hashivim/vim-terraform'

" bash tab completion
Plug 'WolfgangMehner/bash-support'

" yaml syntax highlighting better
Plug 'stephpy/vim-yaml'

" Unclear why json highlighting sucks without this


" Golang, for future proofing
" Plug 'fatih/vim-go'

" --------------------------- HTML / CSS ----------------------------
" make jinja templates prettier
Plug 'lepture/vim-jinja'
" CSS color, a multi-syntax context-sensitive color name highlighter
Plug 'ap/vim-css-color'

" --------------------------- python --------------------------------
" tab completion maybe
Plug 'ycm-core/YouCompleteMe'
" should provide better python syntax highlighting :)

" auto linting, docs, etc
Plug 'python-mode/python-mode'
" requirements.text syntax highlighting
Plug 'raimon49/requirements.txt.vim', {'for': 'requirements'}

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
