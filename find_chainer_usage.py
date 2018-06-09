import requests
import re
import time

"""
Prerequisite: Create access tokens
You need private access token to have full access to Github search
API.
Generate your access token in [here](https://github.com/settings/tokens)
you don't need to tick on any access permission because you are not
modifying your private repositories.
"""

# input your token here
token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def range_itr(lst):
    if not lst: return
    lst = list(lst)
    yield "*..%d" % lst[0]
    for i in range(len(lst)-1):
        yield "%d..%d" % (lst[i], lst[i+1])
    yield "%d..*" % lst[-1]


def extract_repo(result):
    return (itm["repository"]["url"] for itm in result.json()["items"])


def query_backoff(*args, **argv):
    max_tries = 5
    wait = 120
    for _ in range(max_tries):
        r = requests.get(*args, **argv)
        if r.status_code == 200:
            return r
        print("Query failed. Wait %d secs and try again: %s" % (wait, r.content))
        time.sleep(wait)
        wait *= 2

def search_all(query):
    headers = {'Authorization': 'token %s' % token}
    base_url = 'https://api.github.com/'
    payload = {'q': query}
    r = query_backoff(base_url + 'search/code', params=payload, headers=headers)
    print("Successful query (%s) with total count %d."  % (r.request.url, r.json()["total_count"]))
    repos = set(extract_repo(r))
    while True:
        if "Link" not in r.headers:
            # when there is only one page
            break
        m = re.match(r'<(.*?)>; rel="next"', r.headers["Link"])
        if m is None:
            break
        # github allows 30 requests per minute, but let there be some margin
        time.sleep(10)
        r = query_backoff(m.group(1), headers= headers)
        repos.update(extract_repo(r))
    return repos

def count_hits(query, size_threshs):
    headers = {'Authorization': 'token %s' % token}
    base_url = 'https://api.github.com/'
    for size in range_itr(size_threshs):
        payload = {'q': query + " size:" + size}
        # github block similar queries, so take extra intervals
        time.sleep(61)
        r = requests.get(base_url + 'search/code', params=payload, headers=headers)
        print("%s: %d" % (size, r.json()["total_count"]))


def retrieve_matched_repo(query, size_threshs):
    repos = set()
    for size in range_itr(size_threshs):
        repos.update(search_all(query + " size:" + size))
    return repos
  
# I used this to find good thresholds      
# count_hits('chainer in:file extension:py', range(1000, 50000, 1000))

threshs = list(range(100, 8000, 100)) + list(range(8000, 20000, 1000))
result = retrieve_matched_repo('chainer in:file extension:py', threshs)

print("Number repos found:", len(result))

with open("found_all.txt", 'w') as fout:
    for r in result:
        fout.write(r + '\n')
