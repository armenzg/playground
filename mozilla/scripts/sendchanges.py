#! /usr/bin/env python
import os

GLOBAL_VARS = {
    'ftp':         'http://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central',
    'master_port': 'dev-master01.build.mozilla.org:9041',
    'platform_vars': {
        'linux64': 'linux-x86_64.tar.bz2',
        'linux': 'linux-i686.tar.bz2',
        'mac': 'mac.dmg',
        'win32': 'win32.zip',
    }
}

def main():
    for platform in ('linux', 'linux64', 'win32', 'mac'):
        sendchange(GLOBAL_VARS['ftp'], platform)

def sendchange(ftp, platform):
    # buildbot sendchange --master buildbot-master10.build.mozilla.org:9301 --username sendchange
    # --branch mozilla-central-linux64-talos --revision a05ecb395410 --comments 'blah blah'
    # --property buildid:20111212132718 --property pgo_build:False --property builduid:3db61ecf7b8f43f980120baeeabbe97a
    # http://stage.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1323725238/firefox-11.0a1.en-US.linux-x86_64.tar.bz2
    #
    # buildbot sendchange --master buildbot-master10.build.mozilla.org:9301 --username sendchange-unittest 
    # --branch mozilla-central-linux64-opt-unittest --revision a05ecb395410 --comments 'blah blah'
    # --property buildid:20111212132718 --property pgo_build:False --property builduid:3db61ecf7b8f43f980120baeeabbe97a
    # http://stage.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1323725238/firefox-11.0a1.en-US.linux-x86_64.tar.bz2
    # http://stage.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/mozilla-central-linux64/1323725238/firefox-11.0a1.en-US.linux-x86_64.tests.zip
    for jobType in ('talos','opt',):
        downloadables = ['%s/firefox-%s.en-US.%s' % \
                        (ftp, current_version(), extension(platform))] 
        if jobType == "talos":
            branch = 'mozilla-central-%s-talos' % platform
            username = 'sendchange'
        elif jobType == "opt":
            branch = 'mozilla-central-%s-opt-unittest' % platform
            downloadables += [' %s/firefox-%s.en-US.%s.tests.zip' % \
                             (ftp, current_version(), extension(platform))] 
            username = 'sendchange-unittest'

        sendchange = "buildbot sendchange " \
            "--master %(master_port)s " \
            "--username %(username)s " \
            "--branch %(branch)s " \
            % {'master_port': GLOBAL_VARS['master_port'],
               'branch':      branch, 
               'username':    username,
            }
        for d in downloadables:
            sendchange += d
        os.system(sendchange)

def current_version():
    return '11.0a1'

def extension(platform):
    return GLOBAL_VARS['platform_vars'][platform]

if __name__ == '__main__':
    main()
