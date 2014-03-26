export PATH=/opt:$PATH
export PYTHONPATH=~/repos/tools/lib/python:~/repos:$PYTHONPATH

export PEOPLE='people.mozilla.com:~/public_html/incoming'
export DEV='dev-master01:~/moz/patches'
# What is the purpose of this line?
#export PROMPT_COMMAND='history -a; history -r'

# Where did I get this code from?
function parse_git_dirty {
  [[ $(git status 2> /dev/null | tail -n1) != nothing* ]] && echo "*"
}
function parse_git_branch {
  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/[\1$(parse_git_dirty)]/"
}


function hg_dirty {
    hg status --no-color 2> /dev/null \
    | awk '$1 == "?" { print "?" } $1 != "?" { print "!" }' \
    | sort | uniq | head -c1
}

function parse_hg_branch {
    hg branch 2> /dev/null | awk '{print $1}'
}

parse_branch_repo() {
    {
    git_root=$(parse_git_branch)
    if [[ $git_root != "" ]] 
    then
        echo -n "git:$git_root "
    fi
    hg_branch=`parse_hg_branch`
    if [[ "$hg_branch" != "" ]]
    then
        echo -n "hg:[$hg_branch$(hg_dirty)] "
    fi
    }
}

export PS1="\[\033[00m\]\h\[\033[01;34m\] \W \[\033[31m\]\$(parse_branch_repo)\[\033[00m\]$\[\033[00m\] "
