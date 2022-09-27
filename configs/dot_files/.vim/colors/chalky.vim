" Vim color scheme
"
" Name:         chalky.vim
" Maintainer:   @jessebot 
" Last Change:  2022-09-27 13:29:11.0 +0000 
" License:      GPLv3

set background=dark
hi clear
if exists("syntax_on")
   syntax reset
endif

let g:colors_name = "chalky"

" Colours in use
" --------------
" #FF5600 bright orange
" #FFDE00 yolk yellow
" #D8FA3C lemon yellow
" #87ce6a green
" #4ea9ff light blue
" #95adef faded blue

if has("gui_running")
  "GUI Colors
  highlight Normal guifg=White   guibg=#2A2A40
  highlight Cursor guifg=Black   guibg=Yellow
  highlight CursorLine guibg=#191E2F
  highlight LineNr guibg=#323232 guifg=#888888
  highlight Folded guifg=#1d2652 guibg=#2A2A40
  highlight Pmenu guibg=#4ea9ff
  highlight Visual guibg=#283A76

  "General Colors
  highlight Comment guifg=#95adef
  highlight Constant guifg=#D8FA3C
  highlight Keyword guifg=#FFDE00
  highlight String guifg=#87ce6a
  highlight Type guifg=#4ea9ff
  highlight Identifier guifg=#87ce6a gui=NONE
  highlight Function guifg=#FF5600 gui=NONE
  highlight clear Search
  highlight Search guibg=#1C3B79
  highlight PreProc guifg=#FF5600

  " StatusLine
  highlight StatusLine  guifg=#000000 guibg=#ffffaf gui=italic
  highlight StatusLineNC  guifg=#000000 guibg=#ffffff gui=NONE

  "Invisible character colors
  highlight NonText guifg=#4a4a59
  highlight SpecialKey guifg=#4a4a59

  "HTML Colors
  highlight link htmlTag Type
  highlight link htmlEndTag htmlTag
  highlight link htmlTagName htmlTag

  "Ruby Colors
  highlight link rubyClass Keyword
  highlight link rubyDefine Keyword
  highlight link rubyConstant Type
  highlight link rubySymbol Constant
  highlight link rubyStringDelimiter rubyString
  highlight link rubyInclude Keyword
  highlight link rubyAttribute Keyword
  highlight link rubyInstanceVariable Normal

  "Rails Colors
  highlight link railsMethod Type

  "Sass colors
  highlight link sassMixin Keyword
  highlight link sassMixing Constant

  "Outliner colors
  highlight OL1 guifg=#FF5600
  highlight OL2 guifg=#87ce6a
  highlight OL3 guifg=#4ea9ff
  highlight OL4 guifg=#D8FA3C
  highlight BT1 guifg=#95adef
  highlight link BT2 BT1
  highlight link BT3 BT1
  highlight link BT4 BT1

  "Markdown colors
  highlight markdownCode guifg=#87ce6a guibg=#2A2A40
  highlight link markdownCodeBlock markdownCode

  "Git colors
  highlight gitcommitSelectedFile guifg=#87ce6a
  highlight gitcommitDiscardedFile guifg=#C23621
  highlight gitcommitWarning guifg=#C23621
  highlight gitcommitBranch guifg=#FFDE00
  highlight gitcommitHeader guifg=#4ea9ff

end
