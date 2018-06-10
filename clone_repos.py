import requests
import re
import os
import re
import json
from time import sleep
from subprocess import call
import argparse

# input your token here
token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def query_backoff(*args, **argv):
    max_tries = 5
    wait = 120
    for _ in range(max_tries):
        r = requests.get(*args, **argv)
        if r.status_code == 200:
            return r
        elif r.status_code == 404:
            return None
        print("Query failed. Wait %d secs and try again: %s" % (wait, r.content))
        time.sleep(wait)
        wait *= 2

p = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument('REPO_LIST_PATH', type=str)
parser.add_argument('OUT_PATH', type=str)
parser.add_argument('--filter', type=str, default=None,
                    help="remove all python files but the give argument")
args = parser.parse_args()


if args.filter is not None:
    # join with spaces because of shell=True
    cmd_filter = " ".join(
        ["find", out_path, "-type", "f", "!", "-name", "README*", "-print0", "|",
         "xargs", "--null", "grep", "-Z", "-L", args.filter, "|",
         "xargs", "--null", "rm", "-f"])
else:
    cmd_filter = " ".join(
        ["find", out_path, "-type", "f", "!", "-name", "README*",  "!", "-name", "*.py", "-print0", "|",
         "xargs", "--null", "rm", "-f"])


with open(args.REPO_LIST_PATH) as fin:
    #for i, api_url in enumerate(fin):
    #    if i == 3352:
    #        break
    #i = 3311
    i = 0
    for api_url in fin:
        headers = {'Authorization': 'token %s' % token}
        r = query_backoff(api_url.strip(), headers=headers)
        if r is None:
            print("URL not found, probably a deleted repo")
            continue
        clone_url_splitted = r.json()["clone_url"].split("/")
        clone_url = "git@github.com:%s/%s" % (clone_url_splitted[-2], clone_url_splitted[-1])
        out_dir = os.path.join(args.OUT_PATH, str(i))
        os.makedirs(out_dir)
        with open(os.path.join(out_dir, "api.json"), "w") as fout:
            json.dump(r.json(), fout, indent=2)
        out_path = os.path.join(args.OUT_PATH, str(i), clone_url_splitted[-1][:-4])

        call(["git", "clone", "--depth", "1", clone_url, out_path])
        # delete .git dir
        call(["rm", "-rf", os.path.join(out_path, ".git")])
        # delete everything except python files
        call(["find", out_path, "-type", "f", "!", "-name", "README*", "!", "-name", "*.py", "-delete"])

        call(cmd_filter, shell=True)
        i += 1
        sleep(2)

