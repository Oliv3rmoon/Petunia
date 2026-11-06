#!/usr/bin/env python3
# Petunia - The app's name, title ID, data folder and release repository, from param.json alone.
# Copyright (C) 2026 Oliv3rmoon
# SPDX-License-Identifier: GPL-3.0-or-later
"""usage: tools/app-identity.py [--defines | --get NAME]

sce_sys/param.json is the one place the app's name (titleName) and title ID are written. The
build hands them to the code as definitions (tools/build.sh, tools/run_clang_tidy.sh); the
folder the app keeps its data in and the GitHub repository whose releases the update check
offers follow from the name:

    APP_TITLE_NAME         "Petunia"             titleName
    APP_TITLE_ID           "PPSA99017"           titleId
    APP_DATA_NAME          "petunia"             the name in lower case, letters and digits only:
                                                 /data/petunia, logs/petunia.log
    APP_UPDATE_REPOSITORY  "Oliv3rmoon/Petunia"  OWNER/the name, spaces as "-"

--defines prints them as compiler arguments, one a line; --get prints one value. Renaming the
app is `make init TITLE_ID=<its title> APP_NAME="<new name>" APP_CATEGORY=media`, which rewrites
param.json; the README and the docs say the name in prose and are edited by hand. A released
app keeps its name: a new one moves the data folder and the repository it asks for updates.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Whose GitHub releases the update check offers (third_party/update_check/github_release.h).
OWNER = "Oliv3rmoon"


def identity(path=ROOT / "sce_sys/param.json"):
    with open(path, encoding="utf-8") as source:
        param = json.load(source)
    localized = param.get("localizedParameters", {})
    name = localized.get(localized.get("defaultLanguage", ""), {}).get("titleName", "")
    title = param.get("titleId", "")
    # The name goes into C string literals, file names and a repository's name: plain words.
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9]+( [A-Za-z0-9]+)*", name) \
            or len(name) > 32:
        raise SystemExit("param.json titleName must be words of letters and digits, at most 32 "
                         "characters, for tools/app-identity.py")
    if not re.fullmatch(r"PPSA\d{5}", title):
        raise SystemExit("param.json titleId must use PPSA followed by five digits")
    return {
        "APP_TITLE_NAME": name,
        "APP_TITLE_ID": title,
        "APP_DATA_NAME": re.sub(r"[^a-z0-9]", "", name.lower()),
        "APP_UPDATE_REPOSITORY": f"{OWNER}/{name.replace(' ', '-')}",
    }


def main(arguments):
    values = identity()
    if arguments in ([], ["--defines"]):
        for key, value in values.items():
            print(f'-D{key}="{value}"')
    elif len(arguments) == 2 and arguments[0] == "--get" and arguments[1] in values:
        print(values[arguments[1]])
    else:
        raise SystemExit(__doc__.split("\n\n", 1)[0])


if __name__ == "__main__":
    main(sys.argv[1:])
