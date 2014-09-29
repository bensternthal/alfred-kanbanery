# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Script For Alfred To Add Cards To Kanbanery cobbled together by <ben@sternthal.org>

import argparse
import sys
import urllib
import urllib2


parser = argparse.ArgumentParser(description='Script To Add Cards To Kanbanery')
parser.add_argument('--workspace', default=None, help='Kanbanery Workspace')
parser.add_argument('--apikey', default=None, help='Kanbanery API Key')
parser.add_argument('--projectid', default=None, help='Kanbanery Project ID')
parser.add_argument('--text', default=None, help='Text From Alfred')
args = parser.parse_args()

api_endpoint = 'https://%s.kanbanery.com/api/v1/projects/%s/tasks.json' % (args.workspace, args.projectid)

# Seperate 'text' into tuple using ';'. [0] = Card Title, [2] = Card Description
card_data = args.text.partition(";")

def addCard():
    req = urllib2.Request(api_endpoint)
    req.add_header('X-Kanbanery-ApiToken', args.apikey)
    req.add_header('Accept', 'application/json')
    req.add_header("Content-type", "application/x-www-form-urlencoded")

    query_args = { '[task]title': card_data[0], '[task]description': card_data[2] }
    encoded_args = urllib.urlencode(query_args)

    try:
       response = urllib2.urlopen(req, encoded_args)
       print 'Card Added'
    except urllib2.HTTPError, err:
       if err.code == 404:
           print 'Page Not Found'
       elif err.code == 401:
           print 'Access Denied'
       else:
           print 'Error Occured - Error code', err.code
    except urllib2.URLError, err:
        print 'Bizarro Error', err.reason

addCard()

