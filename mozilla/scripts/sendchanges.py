#! /usr/bin/env python
import os

GLOBAL_VARS = {
    'ftp':         'http://ftp.mozilla.org/pub/mozilla.org/firefox/tinderbox-builds/',
    'branch':      'mozilla-central',
    'master_port': 'dev-master01.build.mozilla.org:9041',
    'platform_vars': {
        'linux64': {
            'arch': 'linux-x86_64',
            'ext': 'tar.bz2',
        },
        'linux': { 
            'arch': 'linux-i686',
            'ext': 'tar.bz2',
        },
        'mac': { 
            'arch': 'macosx64',
            'ext': 'dmg',
        },
        'win32': { 
            'arch': 'win32',
            'ext': 'zip',
        }
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
        # XXX: 'base' would fail for debug builds
        base = '%s/%s-%s/%s/firefox-%s.en-US' % (ftp, GLOBAL_VARS["branch"], platform, \
                                                 timestamp(platform), current_version())
        downloadables = ['%s.%s' % \
                        (base, pf_info(platform, 'ext'))] 
        if jobType == "talos":
            branch = 'mozilla-central-%s-talos' % platform
            username = 'sendchange'
        elif jobType == "opt":
            branch = 'mozilla-central-%s-opt-unittest' % platform
            downloadables += [' %s.%s.tests.zip' % \
                             (base, platform)] 
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

def timestamp(platform):
    # Yes, I'm cheating
    if platform == "linux":
        return "1323786259"
    elif platform == "linux64":
        return "1323787701"
    elif platform == "mac":
        return "1323784939"
    elif platform == "win32":
        return "1323785718"

def pf_info(platform, key):
    return GLOBAL_VARS['platform_vars'][platform][key]

if __name__ == '__main__':
    main()
