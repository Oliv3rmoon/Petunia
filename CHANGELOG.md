# Changelog

What changed in each release of Petunia, newest first. A release's notes on GitHub are in
`docs/releases/<version>.md`. What changed in ProsperoRadio before Petunia is on
[bornaradusin/ProsperoRadio's releases](https://github.com/bornaradusin/ProsperoRadio/releases).

## 01.001.000

The first Petunia, based on ProsperoRadio 01.000.010 by BlackBearReloaded, continued by
bornaradusin. A test release. What changed:

- **Its own app.** Petunia is its own title, `PPSA99017`, with its data in `/data/petunia`, so it
  installs beside ProsperoRadio (`PPSA99001`) instead of over it. The name, the title ID and the
  version come from `sce_sys/param.json` alone.
- **The look.** Nightshade's black with chartreuse (#aeea00): near-black pages, black glass
  panels, a chartreuse accent for the main actions and the focus, ink text on it, a near-black sky
  with a low olive glow, and the family's red for "on air".
- **The art.** A new icon, the petunia's trumpet as a speaker horn with three arcs of sound, and
  new home-screen and launch pictures drawn from it (`tools/render-home-art.py`).
- **Credits.** The About page and the About dialog name BlackBearReloaded, who created
  ProsperoRadio, and bornaradusin, who continues it, with Radio Browser, and name nightly, the
  community on Discord.
- **Updates from this repository.** The update check asks GitHub for the newest full release of
  Oliv3rmoon/Petunia instead of the catalog, and installs it with **Update now** after checking
  `PPSA99017.zip` against `SHA256SUMS`. It never offers ProsperoRadio's own releases.
- **Release builds.** A version tag builds, attests and attaches `PPSA99017.zip` and `SHA256SUMS`
  to the tag's draft release; the ps5-opengl SDK is built at the commit ProsperoRadio 01.000.010
  pins.

Playback, the catalogue and the interface are ProsperoRadio 01.000.010's.
