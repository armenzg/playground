alias manage="cd ~/repos/tools; hg pull -u; \
cd buildfarm/maintenance; hg diff manage_masters.py; \
python manage_masters.py -f production-masters.json"

#alias cx='csshX --login cltbld --config ~/.csshX_config'
#alias autoconf='autoconf-2.13'
#alias wget="wget --no-check-certificate"
#alias ssh='ssh -o "StrictHostKeyChecking no"'
#alias top='top -o cpu'
#alias grep='grep -E'
