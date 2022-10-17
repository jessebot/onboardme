" Vim syntax file
" Language:	Python

syn region pythonDocstring  start=+^\s*[uU]\?[rR]\?"""+ end=+"""+ keepend excludenl contains=pythonEscape,@Spell,pythonDoctest,pythonDocTest2,pythonSpaceError
syn region pythonDocstring  start=+^\s*[uU]\?[rR]\?'''+ end=+'''+ keepend excludenl contains=pythonEscape,@Spell,pythonDoctest,pythonDocTest2,pythonSpaceError

hi link pythonDocstring    Comment

syn region pythonVars start="(" skip=+\(".*"\|'.*'\)+ end=")" contained contains=pythonParameters transparent keepend
syn match pythonParameters "[^,]*" contained contains=pythonParam skipwhite
syn match pythonParam "[^,]*" contained contains=pythonExtraOperator,pythonLambdaExpr,pythonBuiltinObj,pythonBuiltinType,pythonConstant,pythonString,pythonNumber,pythonBrackets,pythonSelf,pythonComment skipwhite
syn match pythonExtraOperator "\%([~!^&|/%+-]\|\%(class\s*\)\@<!<<\|<=>\|<=\|\%(<\|\<class\s\+\u\w*\s*\)\@<!<[^<]\@=\|===\|==\|=\~\|>>\|>=\|=\@<!>\|\.\.\.\|\.\.\|::\)"
syn keyword pythonLambdaExpr lambda
syn keyword pythonBuiltinObj True False Ellipsis None NotImplemented
syn keyword pythonBuiltinObj __debug__ __doc__ __file__ __name__ __package__
syn keyword pythonBuiltinType type object
syn keyword pythonBuiltinType str basestring unicode buffer bytearray bytes chr unichr
syn keyword pythonBuiltinType dict int long bool float complex set frozenset list tuple
syn keyword pythonBuiltinType file super
syn region pythonString     start=+[bB]\='+ skip=+\\\\\|\\'\|\\$+ excludenl end=+'+ end=+$+ keepend contains=pythonEscape,pythonEscapeError,@Spell
syn region pythonString     start=+[bB]\="+ skip=+\\\\\|\\"\|\\$+ excludenl end=+"+ end=+$+ keepend contains=pythonEscape,pythonEscapeError,@Spell
syn match   pythonNumber    "\<\d\+[lLjJ]\=\>" display
syn match pythonBrackets "{[(|)]}" contained skipwhite
syn keyword pythonSelf self cls

let g:ycm_enable_semantic_highlighting=1
