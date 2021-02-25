# Author: Clément Notin

import csv
import json

with open("all_groups.json", "r", encoding="utf-8") as f:
    groups = json.load(f)

with open("all_groups.csv", "w", newline="", encoding="utf8") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(("Name", "Visibility", "Teams enabled", "Owners", "Members"))
    csvwriter.writerows([
                            group['displayName'],
                            group['visibility'],
                            group['hasTeams'],
                            ";".join(filter(None, group['owners'])),
                            ";".join(filter(None, group['members'])),
                        ]
                        for group in groups)
