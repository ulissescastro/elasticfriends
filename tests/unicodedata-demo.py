#!/usr/bin/env python
import unicodedata
def sanitize(string):
    try:
        string = string.strip()
        string = unicode(string, 'utf-8')
        string = unicodedata.normalize('NFKD', string).encode('utf-8', 'ignore')
        string = string.lower()
    except Exception, e:
        print string
        print "Sanitize error: %s" % e 
        pass

    return string


def urlize(str):
    url = unicode(str, 'latin-1')
    url = unicodedata.normalize('NFKD', url).encode('ascii', 'ignore')
    url = re.sub(r'[^\w\d-]', '', url.replace(' ', '-').replace('--', '').lower())
    return url

def test(*kwargs):
    for i, j in kwargs.iteritems():
        print i, j

test("a","b","c","d")

