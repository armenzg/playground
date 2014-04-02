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
    #for platform in ('linux64', ):
    for platform in ('win32', ):
        for jobType in ('opt', 'talos', 'debug',):
            sendchange(platform, jobType)

def timestamp(platform, jobType):
    # Yes, I'm cheating
    if   platform == "linux":    return ("1370966894" if jobType == "debug" else "1391715302")
    # mozilla-inbound
    #elif platform == "linux64":  return ("1382722895" if jobType == "debug" else "1391715302")
    # cedar
    elif platform == "linux64":  return ("1391440663" if jobType == "debug" else "1391440663")
    elif platform == "macosx64": return ("1360768805" if jobType == "debug" else "1360779701")
    # mozilla-central
    #elif platform == "win32":    return ("1395803017" if jobType == "debug" else "1395828123")
    # mozilla-aurora
    elif platform == "win32":    return ("1396465593" if jobType == "debug" else "1396456715")
    # mozilla-beta
    #elif platform == "win32":    return ("1396027354" if jobType == "debug" else "1396027354")
    # mozilla-release
    #elif platform == "win32":    return ("1396087950" if jobType == "debug" else "1396087950")
    elif platform == "android":  return ("1336496006" if jobType == "debug" else "1373988789")

def current_version():
    # mozilla-central
    #return '31.0a1'
    # mozilla-aurora
    return '30.0a2'
    # mozilla-beta
    #return '29.0'
    # mozilla-release
    #return '28.0'

GLOBAL_VARS = {
    'ftp':    'http://ftp.mozilla.org/pub/mozilla.org',
    #'branch': 'mozilla-inbound',
    'branch': 'mozilla-aurora',
    'master': 'dev-master1.build.mozilla.org',
    'ports' : [9041],
    'platform_vars': {
        'linux64':  { 'arch_ftp': 'linux64',  'arch_pkg': 'linux-x86_64', 'ext': 'tar.bz2', },
        'linux':    { 'arch_ftp': 'linux',    'arch_pkg': 'linux-i686',   'ext': 'tar.bz2', },
        'macosx':   { 'arch_ftp': 'macosx32', 'arch_pkg': 'mac',          'ext': 'dmg',     },
        'macosx64': { 'arch_ftp': 'macosx64', 'arch_pkg': 'mac64',        'ext': 'dmg',     },
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
        subdir = "try-builds/%s/try-%s" % ("jmathies@mozilla.com-ef8aa4c447f6", \
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

    sendchanges = []
    for p in GLOBAL_VARS["ports"]:
        s = "buildbot sendchange " \
        "--master %(master)s:%(port)s " \
        "--username %(username)s " \
        "--branch %(branch)s " \
        "--revision default " \
        % {'master':   GLOBAL_VARS['master'],
           'port':     p,
           'branch':   scBranch,
           'username': username,
        }
        for d in downloadables:
            if not check_url(d):
                print "You are trying to download a file that does not exist: %s" % d
                sys.exit(1)
            s += " %s" % d
        sendchanges.append(s)

    for s in sendchanges:
        os.system(s)
        print s

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
