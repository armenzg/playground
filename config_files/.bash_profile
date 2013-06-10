. ~/.profile
export PATH=/usr/local/share/python:~/moz/scripts:/usr/local/mysql/bin:/usr/local/bin:$PATH

export PYTHONPATH=$PYTHONPATH:~/repos/tools/lib/python:~/repos:~/repos/releng/buildbot/master
export PEOPLE='people.mozilla.com:~/public_html/incoming'
export H13='jyouthon@youthontherock.com'
export OMID='jyouthon@youthontherock.com:www/resources/video/farsi/satellite'
export DEV='dev-master01:~/moz/patches'
export SDK_HOME=$HOME/moz/sdks/android-sdk-macosx
export PATH=$SDK_HOME/platform-tools:$PATH

alias cx='csshX --login cltbld --config ~/.csshX_config'
alias autoconf='autoconf-2.13'
alias wget="wget --no-check-certificate"
alias manage="cd ~/repos/tools; hg pull -u; \
cd buildfarm/maintenance; hg diff manage_masters.py; \
python manage_masters.py -f production-masters.json"
alias ssh='ssh -o "StrictHostKeyChecking no"'
alias top='top -o cpu'
alias grep='grep -E'

#alias dump_master='~/repos/releng/braindump/buildbot-related/dump_master.py'
#alias dump_masters='~/repos/releng/braindump/buildbot-related/dump_masters.sh'
#export PS1="\u-laptop $ "
#export PATH=~/moz/scripts:~/repos/releng/braindump/buildbot-related:/usr/local/mysql/bin:$PATH
#export WORKON_HOME=$HOME/.virtualenvs
#VIRTUALENVWRAPPER_PYTHON=$HOME/venv/bin/python
#source $HOME/venv/bin/virtualenvwrapper.sh
#export PATH=$HOME/venv/virtualenv-1.8.4/scripts:$PATH

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
