<p align="center">
  <img src="assets/branding/petunia-logo-1024.png" width="160" alt="Petunia logo">
</p>

<h1 align="center">Petunia</h1>

<p align="center">
  <strong>Internet radio on your PS5: tens of thousands of stations, in Nightshade's black with chartreuse.</strong>
</p>

<p align="center">
  Based on <a href="https://github.com/bornaradusin/ProsperoRadio"><strong>ProsperoRadio</strong></a>, created by <strong>BlackBearReloaded</strong> and continued by <a href="https://github.com/bornaradusin"><strong>bornaradusin</strong></a>
</p>

<p align="center">
  <a href="https://github.com/Oliv3rmoon/Petunia/releases"><img src="https://img.shields.io/github/v/release/Oliv3rmoon/Petunia?include_prereleases" alt="Latest release"></a>
  <a href="https://discord.gg/pSqgRU3YP9"><img src="https://img.shields.io/badge/discord-join%20nightly-5865F2?logo=discord&logoColor=white" alt="Discord: join nightly"></a>
  <a href="https://github.com/Oliv3rmoon/Petunia/stargazers"><img src="https://img.shields.io/github/stars/Oliv3rmoon/Petunia?style=social" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0--or--later-blue" alt="License: GPL-3.0-or-later"></a>
  <a href="https://buymeacoffee.com/oliv3rmoon"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-e5484d?logo=buymeacoffee&logoColor=white" alt="Buy me a coffee"></a>
</p>

<p align="center">
  <a href="https://github.com/Oliv3rmoon/Petunia/releases"><strong>Download from the Releases page</strong></a><br>
  Test builds are marked pre-release.
</p>

<p align="center">If Petunia works for you, a ⭐ helps other PS5 owners find it.</p>

Petunia is a native internet-radio app for the PS5, and a Nightshade app by **[Oliv3rmoon](https://github.com/Oliv3rmoon)**: browse and search the free [Radio Browser](https://www.radio-browser.info/) catalogue, keep your favourites, and listen with the console's own audio decoding. It is ProsperoRadio with Nightshade's look and its own updates. The first release is **01.001.000**, a test release; what changed is in the [changelog](CHANGELOG.md).

## Why Petunia

- **Thousands of stations, found fast.** Popular, Trending, Top rated, Favorites and Discover views, and search by text, country, genre, language and bitrate, with mirror failover and server-side paging.
- **A catalogue that stays.** A large SQLite catalogue and your favourites are kept on the console; a failed refresh leaves the last good catalogue untouched, so the app opens straight away offline.
- **Made for the couch.** DualSense D-pad or left stick everywhere, the PS5 keyboard for text, and station names in every script (Arabic, Cyrillic, Chinese, Persian and more) with the console's own fonts and right-to-left ordering.
- **Native PS5 audio.** AAC and AAC+ and MP3 through the console's decoders, Opus through its Opus decoder, Vorbis and FLAC through bounded decoders; M3U and PLS playlists, ICY metadata and audio-only AAC HLS.
- **Nightshade's look.** Black glass panels, a chartreuse accent, a near-black sky with a low olive glow, and the petunia, a trumpet flower like a speaker horn, on the icon and the home-screen pictures.
- **Updates from its own releases.** At the start it asks this repository for a newer release, shows its notes and installs it with **Update now**, after checking the ZIP against `SHA256SUMS`.

## Petunia and ProsperoRadio

Petunia is its own title, `PPSA99017`, so it installs **beside** ProsperoRadio (`PPSA99001`) instead of over it, and keeps its own data in `/data/petunia`. Your ProsperoRadio favourites and settings stay where they are and are not shared with Petunia. The playback, catalogue and interface are ProsperoRadio 01.000.010's; what Petunia changes is the name, the title, the look, the icon and pictures, the About page and the update source.

## Install

You need a PS5 with a compatible homebrew environment and title loader already set up, such as ShadowMountPlus. Petunia does not install or provide an exploit.

1. Close Petunia if it is running.
2. From the [Releases page](https://github.com/Oliv3rmoon/Petunia/releases), download `PPSA99017.zip`.
3. Extract it on your computer, then upload the whole `PPSA99017/` folder over FTP so it ends up at `/data/homebrew/PPSA99017/`, and wait for the transfer to finish. Do not upload the ZIP itself.
4. Let ShadowMountPlus discover `PPSA99017` (restart it cleanly, or restart the PS5), then launch **Petunia** and check the version on its About page.

Don't relaunch the instant you replace the app: ShadowMountPlus may still have the previous folder mounted. Your catalogue, favourites and settings are in `/data/petunia`, outside the app folder, so an update keeps them.

### Updates

Once per launch Petunia asks GitHub for the newest release of [Oliv3rmoon/Petunia](https://github.com/Oliv3rmoon/Petunia/releases) that is not a pre-release. When it is newer than the one installed and carries `PPSA99017.zip` and `SHA256SUMS`, the app offers **Update now**, **What's new** and **Skip**; **Update now** downloads the ZIP, checks it against `SHA256SUMS`, and replaces the app's files once it has closed. Your data in `/data/petunia` is not touched. It needs filesystem access (a resident Lapy service, or the console's payload loader on port 9021); otherwise update by copying the folder as above. Test builds are pre-releases, so the app never offers them: install those by hand. A release ZIP built by this repository's workflow can be checked with `gh attestation verify PPSA99017.zip -R Oliv3rmoon/Petunia`.

### Where Petunia keeps its files

The app itself stays in `/data/homebrew/PPSA99017` (or wherever ShadowMountPlus mounts it from). Everything it writes is in `/data/petunia`:

```text
/data/petunia/
├── config/     settings.txt, the favourites, the update check's state
├── catalog/    the station catalogue (rebuilt by a refresh)
└── logs/       petunia.log and the previous session's
```

Without filesystem access (no resident Lapy service and no ELF loader on port 9021) the same files stay in the title's own storage, `/download0`.

## Docs

| For | Start here |
| --- | --- |
| **Listeners** | [Troubleshooting](docs/TROUBLESHOOTING.md) · [Configuration](docs/CONFIGURATION.md) · [Deployment](docs/DEPLOYMENT.md) |
| **Developers** | [Getting started](docs/GETTING_STARTED.md) · [Architecture](docs/ARCHITECTURE.md) · [Testing](docs/TESTING.md) · [Codec investigation](docs/CODEC_INVESTIGATION.md) |
| **Maintainers** | [Release ZIP](docs/RELEASE_ZIP.md) · [Pull request builds](docs/PULL_REQUEST_BUILDS.md) · [Presentation assets](docs/PRESENTATION_ASSETS.md) · [Contributing](CONTRIBUTING.md) |
| **Project** | [Changelog](CHANGELOG.md) · [Roadmap](ROADMAP.md) · [Third-party notices](THIRD_PARTY_NOTICES.md) |

## Build

Build from Linux, WSL or a Linux CI runner; [Getting started](docs/GETTING_STARTED.md) lists the packages. The build downloads, verifies and caches the public PS5 Payload SDK and the other inputs below the ignored `.deps/`; no proprietary SDK, system module, key or game asset is included or fetched.

```bash
make app     # the complete title folder, dist/PPSA99017/
make test    # host unit tests and the codec, catalogue and update-check checks
make lint    # formatting, static analysis, metadata and shell checks
```

`sce_sys/param.json` is the one place the name, the title ID and the version are written: the build gives the name and title to the code (`tools/app-identity.py`), and the data folder and update repository follow from the name. Keep `PPSA99017` when updating Petunia: changing it makes a separate PS5 title. Release builds come from a version tag (`.github/workflows/tooling.yml`), which attaches the attested ZIP and `SHA256SUMS` to the tag's draft release.

## Requests, bugs and support

- **Ask for a fix or a feature:** [open an issue](https://github.com/Oliv3rmoon/Petunia/issues/new/choose), or ask in **[nightly on Discord](https://discord.gg/pSqgRU3YP9)**.
- **Bugs in my releases:** open an issue here, with `logs/petunia.log` from `/data/petunia` if you can. Leave anything private out.
- **If my work helps you,** you can [buy me a coffee](https://buymeacoffee.com/oliv3rmoon).

## The Nightshade family

Petunia is one of eight repositories in the Nightshade family, all by [Oliv3rmoon](https://github.com/Oliv3rmoon): the same black look, one Discord.

| App | What it is |
| --- | --- |
| [**Nightshade**](https://github.com/Oliv3rmoon/Nightshade) | The Switch emulator for PS5 homebrew |
| [**Physalis**](https://github.com/Oliv3rmoon/Physalis) | Live TV, movies and Plex on the PS5 |
| [**Datura**](https://github.com/Oliv3rmoon/Datura) | Game streaming from your PC to the PS5 |
| **Petunia** (this repo) | Internet radio on the PS5 |
| [**Mandrake**](https://github.com/Oliv3rmoon/Mandrake) | PS1 emulation, with two emulators |
| [**Dulcamara**](https://github.com/Oliv3rmoon/Dulcamara) | RPG Maker 2000 and 2003 games, and Ren'Py visual novels |
| [**Solanum**](https://github.com/Oliv3rmoon/Solanum) | A store for open-source PS5 homebrew, with its catalog [on the web](https://oliv3rmoon.github.io/Solanum-Catalog/) |
| [**Belladonna**](https://github.com/Oliv3rmoon/Belladonna) | Nightshade's PS5 Vulkan driver |

## Built on

[ProsperoRadio](https://github.com/bornaradusin/ProsperoRadio) 01.000.010, created by BlackBearReloaded and continued by bornaradusin.

## Credits

- **ProsperoRadio** was **created and written by BlackBearReloaded**, who made the app, its
  playback, catalogue and interface. All credit for the application and its development is
  theirs; they have since stepped down.
- **[bornaradusin](https://github.com/bornaradusin)** preserved ProsperoRadio when its original
  repository became unavailable, and **continues and maintains it** at
  [bornaradusin/ProsperoRadio](https://github.com/bornaradusin/ProsperoRadio), whose history this
  repository carries. You can support their work through
  [Buy Me a Coffee](https://www.buymeacoffee.com/bornaradusin).
- **[Radio Browser](https://www.radio-browser.info/)**, the free and open community catalogue that
  powers the stations, metadata, search and discovery. Thank you to its maintainers and
  contributors.
- **[Nightshade](https://github.com/Oliv3rmoon/Nightshade)**, Physalis and Datura, whose palette,
  art code and GitHub update check this release reuses.
- Built with the [PS5 Payload SDK](https://github.com/ps5-payload-dev/sdk) by John Törnblom
  (ps5-payload-dev). Filesystem access uses [PS5-Lapy-JB-Daemon](https://github.com/ArkSama/PS5-Lapy-JB-Daemon)
  by ArkSama. Third-party components, authors and licenses are listed in
  [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Thanks to the testers in the nightly Discord, who asked for Petunia and try every test build.

## License

Petunia is an unofficial release. ProsperoRadio is made by BlackBearReloaded and continued by bornaradusin; neither they, Radio Browser, nor Sony endorse Petunia. It is free software under the GNU General Public License, version 3 or later, as ProsperoRadio is ([LICENSE](LICENSE)).

Copyright © 2026 BlackBearReloaded. Petunia's own changes are Copyright © 2026 Oliv3rmoon. Licensed under GPL-3.0-or-later; see [LICENSE](LICENSE). All original copyright notices and third-party acknowledgements are retained, and third-party components keep their own licenses. Binary releases are built from the tagged source in this repository.

## Disclaimer

- **No affiliation.** This is an independent homebrew project. It is not
  affiliated with, endorsed by, or sponsored by Sony Interactive Entertainment.
  "PlayStation", "PS5" and related marks are trademarks of Sony Interactive
  Entertainment Inc.
- **No proprietary material.** No Sony SDK, firmware, encryption keys or
  decrypted system modules are included.
- **Stations are not hosted here.** Radio Browser lists station metadata and
  addresses; the stations stream from their own servers.
- **No warranty.** This project is provided "as is", without warranty of any
  kind, to the extent permitted by law. See sections 15 and 16 of the GPL.
- **Use at your own risk.** Running homebrew requires a modified console, which
  may void its warranty, breach the platform's terms of service, or cause data
  loss.
- **Legal use only.** Use it only with hardware, accounts and content you own.
  This project does not support or enable piracy.

## Help it grow

Like Petunia? **[Star it](https://github.com/Oliv3rmoon/Petunia)** and **[join the Discord](https://discord.gg/pSqgRU3YP9)**.
