#!/usr/bin/env python3
# Petunia - The app's name and title ID are written in param.json alone.
# Copyright (C) 2026 Oliv3rmoon
# SPDX-License-Identifier: GPL-3.0-or-later
"""tools/app-identity.py derives the definitions the build gives the code from
sce_sys/param.json, and no source writes the name or the title ID itself."""

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("app_identity", ROOT / "tools/app-identity.py")
app_identity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_identity)


class AppIdentityTest(unittest.TestCase):
    def test_param_json_names_petunia(self):
        self.assertEqual(app_identity.identity(), {
            "APP_TITLE_NAME": "Petunia",
            "APP_TITLE_ID": "PPSA99017",
            "APP_DATA_NAME": "petunia",
            "APP_UPDATE_REPOSITORY": "Oliv3rmoon/Petunia",
        })

    def test_definitions_for_the_compiler(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/app-identity.py")],
                                capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.splitlines(), [
            '-DAPP_TITLE_NAME="Petunia"',
            '-DAPP_TITLE_ID="PPSA99017"',
            '-DAPP_DATA_NAME="petunia"',
            '-DAPP_UPDATE_REPOSITORY="Oliv3rmoon/Petunia"',
        ])

    def test_names_that_do_not_fit_are_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            param = Path(directory) / "param.json"
            for name in ("", " Petunia", "Petunia ", "Pet  unia", 'Pet"unia', "Pet/unia", "x" * 33):
                param.write_text(json.dumps({
                    "titleId": "PPSA99017",
                    "localizedParameters": {"defaultLanguage": "en-US",
                                            "en-US": {"titleName": name}},
                }), encoding="utf-8")
                with self.assertRaises(SystemExit, msg=repr(name)):
                    app_identity.identity(param)

    def test_the_build_and_the_analysis_use_them(self):
        for script in ("tools/build.sh", "tools/run_clang_tidy.sh"):
            text = (ROOT / script).read_text(encoding="utf-8")
            self.assertIn('identity=$(python3 "$root/tools/app-identity.py" --defines)', text)
            self.assertIn('"${identity_flags[@]}"', text)

    def test_no_source_writes_the_name_or_the_title(self):
        # The name and the title ID come from APP_TITLE_NAME and APP_TITLE_ID; ProsperoRadio's
        # are only named in comments, file headers and credits.
        found = []
        for path in sorted((ROOT / "src").rglob("*")) + sorted((ROOT / "include").rglob("*")):
            if path.suffix not in (".c", ".cc", ".cpp", ".h", ".hpp"):
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                code = line.split("//", 1)[0]
                if code.lstrip().startswith(("*", "/*")):
                    continue
                if re.search(r'"[^"]*(Petunia|PPSA\d{5}|/data/[a-z]+")', code) or \
                        re.search(r'"[^"]*ProsperoRadio[^"]*"', code) and \
                        "release of ProsperoRadio" not in code and "[ProsperoRadio]" not in code:
                    found.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
