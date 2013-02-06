#! /usr/bin/env python
# https://hg.mozilla.org/try/rev/f82b3238c587
# https://hg.mozilla.org/try/json-pushes?full=1&changeset=ab5eb07624b0
import urlparse, urllib#, time
try:
    import json
except:
    import simplejson as json
import urllib2 #, httplib, socket, ssl

#import subprocess
#from buildbotcustom.changes.hgpoller import _parse_changes
#import logging as log

def getChanges(base_url="https://hg.mozilla.org/try/rev/f82b3238c587", last_changeset=None, tips_only=False, ca_certs=None,
        username=None, password=None):
    bits = urlparse.urlparse(base_url)
    #if bits.scheme == 'https':
    #    assert ca_certs, "you must specify ca_certs"

    params = [('full', '1')]
    if last_changeset:
        params.append( ('fromchange', last_changeset) )
    if tips_only:
        params.append( ('tipsonly', '1') )
    url = "%s/json-pushes?%s" % (base_url, urllib.urlencode(params))

    #log.debug("Fetching %s", url)

    #if bits.scheme == 'https':
    #    handle = validating_https_open(url, ca_certs, username, password)
    #else:
    #    handle = urllib2.urlopen(url)
    handle = urllib2.urlopen("https://hg.mozilla.org/try/json-pushes?full=1&changeset=ab5eb07624b0&tipsonly=1")
    #handle = urllib2.urlopen(url)

    data = handle.read()
    return _parse_changes(data)

def _parse_changes(data):
    pushes = json.loads(data)
    changes = []
    for push_id, push_data in pushes.iteritems():
        push_time = push_data['date']
        push_user = push_data['user']
        for cset in push_data['changesets']:
            change = {}
            change['updated'] = push_time
            change['author'] = push_user
            change['changeset'] = cset['node']
            change['files'] = cset['files']
            change['branch'] = cset['branch']
            change['comments'] = cset['desc']
            changes.append(change)

    # Sort by push date
    # Changes in the same push have their order preserved because python list
    # sorts are stable. The leaf of each push is sorted at the end of the list
    # of changes for that push.
    changes.sort(key=lambda c:c['updated'])
    return changes

if __name__ == '__main__':
    c= getChanges()
    for i in c:
       for k in i.keys():
           print k
           if k in ("changeset",):
               print i[k]
