import requests
import re
import time
import datetime
import numpy as np

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

def extract_repo(result):
    return (itm["url"] for itm in result.json()["items"])


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


def retrieve_matched_repo(query, num, from_year, to_year=None, n_per_query=5):
    headers = {'Authorization': 'token %s' % token}
    base_url = 'https://api.github.com/'
    from_date = datetime.date(from_year, 1, 1)
    if to_year is None:
        to_date = datetime.date.today()
    else:
        to_date = datetime.date(to_year, 1, 1)
    date_diff = (to_date - from_date).days
    date_list = [from_date + datetime.timedelta(days=d) for d in np.random.choice(date_diff, size=(num // n_per_query, ))]
    repos = []
    for date in date_list:
        yestarday = date - datetime.timedelta(days=7)
        payload = {
            'q': query +
            " sort:updated" +
            " created:%d-%02d-%02d..%d-%02d-%02d" % (yestarday.year, yestarday.month, yestarday.day, date.year, date.month, date.day)}

        # github block similar queries, so take extra intervals
        time.sleep(20)
        r = requests.get(base_url + 'search/repositories', params=payload, headers=headers)
        repos.extend(list(extract_repo(r))[:n_per_query])
    return repos

result = retrieve_matched_repo('tensorflow language:python', 200, 2015)

with open("found_all_tensorflow.txt", 'w') as fout:
    for r in result:
        fout.write(r + '\n')


result = retrieve_matched_repo('pytorch language:python', 200, 2017)

with open("found_all_pytorch.txt", 'w') as fout:
    for r in result:
        fout.write(r + '\n')
