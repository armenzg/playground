. ~/.profile
export PATH=~/moz/scripts:/usr/local/mysql/bin:$PATH

#export PYTHONPATH=$PYTHONPATH:~/repos/tools/lib/python:~/repos
export PEOPLE='people.mozilla.com:~/public_html/incoming'
export HECHOS13='jyouthon@youthontherock.com:www/hechos13/incoming'
export OMID='jyouthon@youthontherock.com:www/resources/video/farsi/satellite'

alias cx='csshX --login cltbld --config ~/.csshX_config'
alias autoconf='autoconf-2.13'
alias wget="wget --no-check-certificate"
alias manage="cd ~/repos/tools; hg pull -u; \
hg up -C; cd buildfarm/maintenance; hg diff; \
python manage_masters.py -f production-masters.json"
alias ssh='ssh -o "StrictHostKeyChecking no"'
alias top='top -o cpu'
alias grep='grep -E'

#alias dump_master='~/repos/releng/braindump/buildbot-related/dump_master.py'
#alias dump_masters='~/repos/releng/braindump/buildbot-related/dump_masters.sh'
#export PS1="\u-laptop $ "
#export WORKON_HOME=$HOME/.virtualenvs
#export VIRTUALENVWRAPPER_PYTHON=$HOME/.venv/bin/python
#source $HOME/.venv/bin/virtualenvwrapper.sh
#export PATH=~/moz/scripts:~/repos/releng/braindump/buildbot-related:/usr/local/mysql/bin:$PATH