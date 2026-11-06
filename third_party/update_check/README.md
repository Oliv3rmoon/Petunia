# Update check and self-update

These files are the PS5 Native App Boilerplate's (`examples/update-check` and
`examples/self-update`, boilerplate commit 2966cac), taken as ProsperoEden
carries them: `self_update_ps5.c` takes the paths of the helper, of the app's
`param.json` and of the sequence file from `SELF_UPDATE_HELPER_PATH`,
`SELF_UPDATE_PARAM_PATH` and `SELF_UPDATE_SEQUENCE_PATH` when they are defined.
ProsperoRadio defines them (`src/update_kit/self_update_ps5.c`,
`src/radio_update.cpp`) because its folder is not `/app0` once it runs with
filesystem access.

The boilerplate's `console_curl.c` is not here: ProsperoRadio's radio service
already carries libcurl with the same console stand-ins
(`src/runtime/runtime_shims.c`, `src/runtime/netdb_shims.c`), so the three
functions of `console_curl.h` are implemented beside them in
`src/radio_http_curl.cpp`.

The helper the app sends to the console's payload loader is in
`third_party/self_update_helper` (the boilerplate's
`examples/self-update-helper` with ProsperoEden's three changes: its Makefile's
source folders; `swap_entries` in `updater.cpp`, which moves aside only the
entries the release replaces, so files a listener put in the app folder stay;
and `mounted_source`, which takes the installed folder from ShadowMountPlus's
`/user/app/<TITLEID>/mount.lnk` and refuses an image install).

In the kit itself (ProsperoEden's change), `self_update_check` also copies the
catalog entry's `release_notes` and `release_notes_truncated` into the offer
(`notes`, `notes_truncated`), for the update dialog's What's new view.

## Petunia: updates from GitHub releases

`github_release.{h,c}` are Nightshade's (Oliv3rmoon/Nightshade,
`headless/update_check/github_release.*`), as Nightshade TV and Datura have them, for this
repository's releases: the app asks GitHub for the newest release of the repository it names
(`kUpdateRepository` in `src/radio_update.cpp`, `Oliv3rmoon/Petunia`, from param.json's
`titleName` by `tools/app-identity.py`) instead of the catalog, and fills the same offer, so the
download, the helper and the update dialog are the kit's, unchanged. `src/update_kit/github_release.c`
compiles it into the app. The release must not be a draft or a pre-release, its tag must be a
content version higher than the app's (the workflow tags a release with its `contentVersion`),
and it must carry `PPSA99017.zip` and a `SHA256SUMS` that lists that ZIP on one well-formed
line. Its trust is TLS and the release's own `SHA256SUMS`, not the catalog's signature (see the
header). The app never asks the catalog, which lists ProsperoRadio's own releases: an update from
there would undo the name, the title, the look and this update source; a build naming
ProsperoRadio's own repositories does not compile.

For it, `update_check.c` has three more readers, as Nightshade's kit has them
(`update_check_json_value`, `update_check_json_uint` and `update_check_json_array_next`), and
refuses a NUL inside a string it copies; `self_update_ps5.c` has `self_update_check_self_from`
and `self_update_check_as_from`, and its `console_fetch` tells an answer too long for its buffer
(`SELF_UPDATE_FETCH_TOO_LARGE`) from a failed transfer. The host check is
`tests/github_release_check.cc`, built and run by `tests/test_github_release.py`
(`make test-integration`).

A test build still takes `dev/update-offer.txt` in the app's folder instead of GitHub's answer
(`src/radio_update.cpp`); it skips the release's `SHA256SUMS`.
