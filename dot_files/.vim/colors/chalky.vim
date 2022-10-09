" Vim color scheme
"
" Name:         chalky.vim
" Maintainer:   @jessebot - Jesse Hitch
" Last Change:  2022-10-08 08:18:29.0 +0200
" License:      GPLv3
" Notes: Use this command to check vim help on what variables are called
"         :help 
"        can also use http://bytefluent.com/vivify/ to find variables of colors
"        

" Colours in use
" --------------
" #f289f9 dark magenta
" #ff8d87 soft redish orange
" #fdcd36 light orange
" #f7fb53 soft yellow
" #a8fd57 lime green
" #5ac4b9 teal
" #5cc9fd light blue
" #a3a8f8 medium purple
"
" #232336 blueish black
" #2569aa darker blue
" #f2748a pale red

set background=dark

hi clear

if exists("syntax_on")
   syntax reset
endif
hi Search ctermbg=White
hi Search ctermfg=DarkBlue

let g:colors_name = "chalky"

" GUI Colors
highlight Normal      guifg=White   guibg=#232336
highlight Cursor      guifg=Black   guibg=Yellow
highlight CursorLine  guibg=#191E2F
highlight LineNr      guibg=#323232 guifg=#888888
highlight Folded      guifg=#1d2652 guibg=#232336
highlight Visual      guibg=#283A76

" this one controls the column over 80 characters
highlight ColorColumn guibg=#2569aa

" these are for little popup dropdown menus, for things like tab complete
highlight Pmenu    guibg=#5cc9fd guifg=#000000
highlight PMenuSel guibg=#2569aa guifg=white

" General Colors
highlight Comment    guifg=#a3a8f8
highlight Constant   guifg=#f7fb53
highlight Keyword    guifg=#fdcd36
highlight String     guifg=#a8fd57
highlight Boolean    guifg=#5ac4b9
highlight Number     guifg=#5ac4b9
highlight Float      guifg=#5ac4b9
highlight Type       guifg=#5cc9fd
highlight Identifier guifg=#a8fd57 gui=NONE
highlight Function   guifg=#5cc9fd gui=NONE
highlight PreProc    guifg=#f289f9

" Searching
highlight clear Search
highlight Search     guibg=#f7fb53 guifg=Black

" Invisible character colors
highlight NonText    guifg=#4a4a59
highlight SpecialKey guifg=#4a4a59

" HTML Colors
highlight link htmlTag     Type
highlight link htmlEndTag  htmlTag
highlight link htmlTagName htmlTag

" Ruby Colors
highlight link rubyClass            Keyword
highlight link rubyDefine           Keyword
highlight link rubyConstant         Type
highlight link rubySymbol           Constant
highlight link rubyStringDelimiter  rubyString
highlight link rubyInclude          Keyword
highlight link rubyAttribute        Keyword
highlight link rubyInstanceVariable Normal

" Rails Colors
highlight link railsMethod Type

" Sass colors
highlight link sassMixin Keyword
highlight link sassMixing Constant

" Outliner colors
highlight OL1 guifg=#f289f9
highlight OL2 guifg=#a8fd57
highlight OL3 guifg=#5cc9fd
highlight OL4 guifg=#f7fb53
highlight BT1 guifg=#a3a8f8
highlight link BT2 BT1
highlight link BT3 BT1
highlight link BT4 BT1

" Markdown colors
highlight markdownCode guifg=#a8fd57 guibg=#232336
highlight link markdownCodeBlock markdownCode

" Git colors
highlight gitcommitSelectedFile  guifg=#a8fd57
highlight gitcommitDiscardedFile guifg=#f2748a
highlight gitcommitWarning       guifg=#f2748a
highlight gitcommitBranch        guifg=#fdcd36
highlight gitcommitHeader        guifg=#5cc9fd

" Gitgutter stuff
highlight! link SignColumn LineNr
" change sign color color
highlight SignColumn guibg=#1d1d1d ctermbg=black
" change the colors back to what they should be when there are changes
highlight GitGutterAdd    guifg=#a8fd57 ctermfg=2
highlight GitGutterChange guifg=#f7fb53 ctermfg=3
highlight GitGutterDelete guifg=#f2748a ctermfg=1
