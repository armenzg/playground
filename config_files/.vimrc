set nocompatible
"set autoindent <-- this messes things when pasting content 
"set smartindent <-- this messes things when pasting content
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab
filetype indent on
set showmatch
set guioptions-=T
set vb t_vb=
set ruler
set incsearch
set ignorecase
set smartcase
set number
syntax enable
filetype plugin indent on
set t_Co=16
set t_Co=256
set foldenable
"set fdm=indent <-- adds ugly folding
nnoremap <space> za
set scrolloff=5
set cursorline
set backspace=indent,eol,start
set laststatus=2
set statusline=%F%m%r%h%w\ [TYPE=%Y\ %{&ff}]\ [%l/%L\ (%p%%)]
set history=50
set nohlsearch
set tw=0
set background=light


"Language Specifics
autocmd BufRead,BufNewFile Makefile*,*.mk,*.mk.in set noexpandtab
autocmd BufRead,BufNewFile *py,*pyw,*.cfg set filetype=python
autocmd BufRead,BufNewFile *py,*pyw,*.cfg match BadWhitespace /^t\+/
autocmd BufRead,BufNewFile *py,*pyw,*.cfg match BadWhitespace /\s\+$/
autocmd BufNewFile * set fileformat=unix

highlight BadWhitespace ctermbg=red guibg=red
highlight ExtraWhitespace ctermbg=darkgreen guibg=lightgreen

syn on
set enc=utf-8
set sts=4
set sw=4
set et
" Only do this part when compiled with support for autocommands
if has("autocmd")
  " In text files, always limit the width of text to 78 characters
  autocmd BufRead *.txt set tw=78
  " When editing a file, always jump to the last cursor position
  autocmd BufReadPost *
  \ if line("'\"") > 0 && line ("'\"") <= line("$") |
  \   exe "normal! g'\"" |
  \ endif
endif

autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS
autocmd FileType xml set omnifunc=xmlcomplete#CompleteTags
autocmd FileType php set omnifunc=phpcomplete#CompletePHP
autocmd FileType c set omnifunc=ccomplete#Complete

execute pathogen#infect()
