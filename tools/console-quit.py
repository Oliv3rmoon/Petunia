#!/usr/bin/env python3
# ProsperoRadio - Ask the running app on a console to close itself, and wait.
# Copyright (C) 2026 BlackBearReloaded
# SPDX-License-Identifier: GPL-3.0-or-later
"""usage: tools/console-quit.py <host> [seconds to wait, default 60]

Puts dev/quit.txt beside the installed app (a test build closes itself within
a second of seeing it), waits for the title to be gone, and removes the file.
It never kills anything: if the app stays, it says so.
"""
import io
import sys
import time
from ftplib import FTP, all_errors
from pathlib import Path

# Petunia: the title and the data folder's name come from param.json (tools/app-identity.py).
sys.path.insert(0, str(Path(__file__).resolve().parent))
IDENTITY = __import__("app-identity").identity()
TITLE = IDENTITY["APP_TITLE_ID"]
PATH = f"/data/homebrew/{TITLE}/dev/quit.txt"


def session(host):
    ftp = FTP()
    ftp.connect(host, 2121, timeout=20)
    ftp.login("anonymous", IDENTITY["APP_DATA_NAME"])
    return ftp


def running(ftp):
    ftp.cwd("/mnt/sandbox")
    names = [name for name, _ in ftp.mlsd()]
    ftp.cwd("/")
    return any(name.startswith(TITLE) for name in names)


def main():
    host = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    ftp = session(host)
    was_running = running(ftp)
    if was_running:
        try:
            ftp.mkd(f"/data/homebrew/{TITLE}/dev")
        except all_errors:
            pass
        ftp.storbinary(f"STOR {PATH}", io.BytesIO(b"close\n"))
    closed = not was_running
    waited = 0
    while not closed and waited < limit:
        time.sleep(3)
        waited += 3
        closed = not running(ftp)
    try:
        ftp.sendcmd(f"DELE {PATH}")  # a leftover would close the next launch at once
    except all_errors:
        pass
    ftp.quit()
    print("not running" if not was_running else
          f"closed after {waited} s" if closed else f"STILL RUNNING after {limit} s")
    sys.exit(0 if closed else 1)


if __name__ == "__main__":
    main()
