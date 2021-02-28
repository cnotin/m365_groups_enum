# Author: Clément Notin

import argparse
import concurrent.futures
import json
import sys
from time import sleep

from requests_oauthlib import OAuth2Session
from roadtools.roadlib.auth import Authentication


def get(graph_client, url):
    while True:
        resp = graph_client.get(url)
        if resp.status_code != 200:
            print(f"Got status code {resp.status_code} for {resp.text}")
            sleep(60)
            continue
        if "application/json" not in resp.headers.get('content-type'):
            print(f"Got wrong content-type {resp.headers.get('content-type')} for {resp.text}")
            sleep(60)
            continue
        if "value" not in resp.json():
            print(f"'value' missing in {resp.json()}")
            sleep(60)
            continue

        return resp.json()


def task(graph_client, group):
    group["hasTeams"] = "Team" in group['resourceProvisioningOptions']

    if len(group['resourceProvisioningOptions']) == 0:
        group['resourceProvisioningOptions'] = None
    else:
        group['resourceProvisioningOptions'] = str(group['resourceProvisioningOptions'])

    group['owners'] = []
    owners = get(graph_client, f"https://graph.microsoft.com/beta/groups/{group['id']}/owners")['value']
    #TODO: handle pagination to get more than 100 owners
    for owner in owners:
        if "mail" in owner:
            group['owners'].append(owner['mail'])
        else:
            group['owners'].append(str(owner))

    group['members'] = []
    members = get(graph_client, f"https://graph.microsoft.com/beta/groups/{group['id']}/members")['value']
    #TODO: handle pagination to get more than 100 members
    for member in members:
        if "mail" in member:
            group['members'].append(member['mail'])
        else:
            group['members'].append(str(member))


def enumerate_groups(graph_client):
    groups = []
    print("Getting all groups... ")
    url = "https://graph.microsoft.com/beta/groups?" \
          "$filter=groupTypes/any(c:c+eq+'Unified')&" \
          "$select=displayName,visibility,id,description,mailEnabled,mail,mailNickname,resourceProvisioningOptions"
    # get more than 100 (by default) groups by implementing pagination
    while True:
        req = get(graph_client, url)
        groups += req['value']
        if '@odata.nextLink' in req:
            url = req['@odata.nextLink']
        else:
            break
    print(f"Got {len(groups)} groups")

    print("Getting groups details...")

    cpt = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = (executor.submit(task, graph_client, group) for group in groups)
        for _ in concurrent.futures.as_completed(futures):
            cpt += 1
            if cpt % 100 == 0:
                print(f"{round(cpt / len(groups) * 100)} %")

    with open("all_groups.json", "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)


if __name__ == '__main__':
    # authentication stuff
    parser = argparse.ArgumentParser(add_help=True, description="FIXME",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    auth = Authentication()
    parser = auth.get_sub_argparse(parser, for_rr=True)
    args = parser.parse_args()
    auth.parse_args(args)
    auth.resource_uri = "https://graph.microsoft.com"
    res = auth.get_tokens(args)
    if not res:
        print("Authentication failed")
        parser.print_help()
        sys.exit(1)
    print(f"Authenticated as {res['userId']}")
    graph_client = OAuth2Session(token={"access_token": res["accessToken"]})

    # main work
    enumerate_groups(graph_client)

    print("Bye!")
