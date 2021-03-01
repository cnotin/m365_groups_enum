# Enumerate Microsoft 365 Groups in a tenant with their metadata

<img src="m365-groups-logo.png" width="200px" height="200px" alt="" />

## Description
The `all_groups.py` script allows to enumerate all Microsoft 365 Groups in a Azure AD tenant with their metadata:
* name
* visibility: public or private
* description
* email address
* owners
* members
* Teams enabled?
* SharePoint URL (e.g. for Teams shared files)

All of this, even for private Groups!
Read more about this on my blog article ["Risks of Microsoft Teams and Microsoft 365 Groups"](https://clement.notin.org/blog/2021/03/02/risks-of-microsoft-teams-and-microsoft-365-groups/)

The `reporting.py` script will take the JSON output from `all_groups.py` and generates a CSV files allowing to quickly identify sensitive private or public groups.

## Installation
Requirement: ![Python 3 only](https://img.shields.io/badge/python-3.6+-blue.svg)

1. Download the repository
2. Install requirements with
```console
pip install -r requirements.txt
```

## Usage
You will need a valid account on the tenant. Different authentication methods are supported:
* via login + password (MFA not supported)
```console
python all_groups.py -u myuser@example.onmicrosoft.com -p MyPassw0rd
```

* via device authentication, which supports MFA via the browser. Launch then follow instructions
```console
python all_groups.py --device-code
```

Other methods are also offered. You can read the [ROADTools documentation](https://github.com/dirkjanm/ROADtools/wiki/Getting-started-with-ROADrecon#authentication) or run the script without any argument to get help.
```console
python all_groups.py
```

That's all, you don't need more options! The script output will be in `all_groups.json` in the current directory.

Then, if you want a nicer and more concise output from this JSON, use `reporting.py` to transform it:
```console
python reporting.py
```
It automatically takes `all_groups.json` in the current directory, and outputs to `all_groups.csv` in the same directory. 

## Acknowledgements
This project uses for authentication the very helpful [roadlib](https://pypi.org/project/roadlib/) from [ROADTools](https://github.com/dirkjanm/ROADtools) by @dirkjanm