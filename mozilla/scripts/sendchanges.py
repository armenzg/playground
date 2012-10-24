#! /usr/bin/env python
import os
import sys
from optparse import OptionParser
import httplib
import urlparse

def main():
    parser = OptionParser()
    (options, args) = parser.parse_args()

    #for platform in ('linux', 'linux64', 'win32', 'macosx64'):
    for platform in ('win32',):
        for jobType in ('talos', 'opt', ):
            sendchange(platform, jobType)

def timestamp(platform, jobType):
    # Yes, I'm cheating
    if   platform == "linux":    return ("1330696599" if jobType == "debug" else "1334247632")
    elif platform == "linux64":  return ("1330427462" if jobType == "debug" else "1338567902")
    elif platform == "macosx64": return ("1330696599" if jobType == "debug" else "1335828641")
    elif platform == "win32":    return ("1346387570" if jobType == "debug" else "1351034355")
    elif platform == "android":  return ("1336496006" if jobType == "debug" else "1336496006")

def current_version():
    return '19.0a1'

GLOBAL_VARS = {
    'ftp':    'http://ftp.mozilla.org/pub/mozilla.org',
    'branch': 'mozilla-central',
    'master': 'dev-master01.build.mozilla.org',
    'port1' : 9041, # for other platforms
    'port2' : 9043, # for android testing
    'platform_vars': {
        'linux64':  { 'arch_ftp': 'linux64',  'arch_pkg': 'linux-x86_64', 'ext': 'tar.bz2', },
        'linux':    { 'arch_ftp': 'linux',    'arch_pkg': 'linux-i686',   'ext': 'tar.bz2', },
        'macosx':   { 'arch_ftp': 'macosx32', 'arch_pkg': 'mac',          'ext': 'dmg',     },
        'macosx64': { 'arch_ftp': 'macosx64', 'arch_pkg': 'mac',          'ext': 'dmg',     },
        'win32':    { 'arch_ftp': 'win32',    'arch_pkg': 'win32',        'ext': 'zip',     },
        'android':  { 'arch_ftp': 'android',  'arch_pkg': 'android-arm',  'ext': 'apk',     },
    }
}

def sendchange(platform, jobType):
    productFtp = "mobile" if platform=="android" else "firefox"
    filename = "fennec-%s.en-US" if platform=="android" else "firefox-%s.en-US"
    branch = GLOBAL_VARS["branch"]
    if branch != "try":
        # e.g. tinderbox-builds/$BRANCH-linux/1334247632
        subdir = "tinderbox-builds/%s-%s/%s" % (branch, ftpLocation(platform, jobType), \
                                                timestamp(platform, jobType))
    else:
        # e.g. try-builds/hurley@mozilla.com-1e3218bc291d/try-linux/ 
        subdir = "try-builds/%s/try-%s" % ("hurley@mozilla.com-1e3218bc291d", \
                                           ftpLocation(platform, jobType))
    base = '%s/%s/%s/%s' % (GLOBAL_VARS["ftp"], productFtp, subdir, filename % current_version())
    downloadables = ['%s.%s.%s' % \
                    (base, pf_info(platform, 'arch_pkg'), pf_info(platform, 'ext'))] 

    if jobType == "talos":
        scBranch = '%s-%s-talos' % (GLOBAL_VARS["branch"], platform)
        username = 'sendchange'
    elif jobType in ("opt", "debug",):
        scBranch = '%s-%s-%s-unittest' % (GLOBAL_VARS["branch"], platform, jobType)
        downloadables += ['%s.%s.tests.zip' % \
                         (base, pf_info(platform, 'arch_pkg'))] 
        username = 'sendchange-unittest'

    sendchange = "buildbot sendchange " \
        "--master %(master)s:%(port)s " \
        "--username %(username)s " \
        "--branch %(branch)s " \
        "--revision default " \
        % {'master':   GLOBAL_VARS['master'],
           'port':     GLOBAL_VARS["port1"] if platform != "android" else GLOBAL_VARS["port2"],
           'branch':   scBranch, 
           'username': username,
        }
    for d in downloadables:
        if not check_url(d):
            print "You are trying to download a file that does not exist: %s" % d
            sys.exit(1)
        sendchange += " %s" % d
    os.system(sendchange)
    print sendchange

# https://pythonadventures.wordpress.com/2010/10/17/check-if-url-exists/
def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None

def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

def ftpLocation(platform, jobType):
    if jobType == "debug":
        return pf_info(platform, 'arch_ftp') + "-debug"
    else:
        return pf_info(platform, 'arch_ftp')

def pf_info(platform, key):
    return GLOBAL_VARS['platform_vars'][platform][key]

if __name__ == '__main__':
    main()
