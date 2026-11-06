# Build output and release ZIP

Every application build creates and validates `dist/<TITLE_ID>/`. That folder is
the only build output:

```bash
make app
```

GitHub Actions also publishes `<TITLE_ID>.zip`. This is not another package
format: it is a standard ZIP containing the complete `dist/<TITLE_ID>/` folder
for users who prefer directory deployment.

## Publishing a release

A release's files come from pushing its version tag: the workflow builds, attests and attaches
the ZIP and `SHA256SUMS`. Release files are not attached by hand, so that every published file
comes from a run and has an attestation. The publish step handles three cases:

- **A release without a ZIP** (a draft made before the tag, as every Petunia release is, or
  notes written in advance): it adds the two files and leaves the title, the notes and the
  state alone, so a draft stays a draft until it is published by hand.
- **No release for the tag:** it creates a draft pre-release with the two files and the notes
  of `docs/releases/<tag>.md` (or the tag's section of `CHANGELOG.md`); a tag alone publishes
  nothing.
- **A release that already has a ZIP:** nothing is replaced or deleted, because the app's
  update check takes the ZIP's SHA-256 from the release's `SHA256SUMS`. The run ends green
  with a warning that those files were not published by it and may have no attestation.

A release ZIP built by the workflow can be checked with
`gh attestation verify PPSA99017.zip -R Oliv3rmoon/Petunia` (GitHub CLI).
