# reefshape-recipes

conda recipes for the packages [ReefShape / ReefMetrics](https://github.com/Tobias-Fischer/reef-metrics)
needs that conda-forge does not have yet, built for all platforms with GitHub
Actions and published to the
[`tobias-fischer/reefshape`](https://prefix.dev/channels/@tobias-fischer/reefshape)
channel on prefix.dev. Recipes are for [rattler-build](https://rattler.build).

Why: until conda-forge merges them, the ReefShape installers (pixi) take these
packages from the `reefshape` channel. Once a recipe is on conda-forge it is removed here.
Pending conda-forge submissions:

| Recipe | staged-recipes PR |
|---|---|
| `py4dgeo` | [#35418](https://github.com/conda-forge/staged-recipes/pull/35418) |
| `cloudcompare` (+ `qcustomplot`, `dxflib`) | [#35422](https://github.com/conda-forge/staged-recipes/pull/35422) |
| `taglab` | [#35457](https://github.com/conda-forge/staged-recipes/pull/35457) |

`pixi-pack-app` is pixi-pack from the owner's fork with `--create-app` (macOS app, Windows
installer, Flatpak; upstream [Quantco/pixi-pack#358](https://github.com/Quantco/pixi-pack/pull/358),
still a draft, so no pixi-pack release has it) plus `pixi-launcher` and `pixi-unpack`; the
ReefShape App workflow installs it from this channel instead of compiling it. Built for
linux-64, linux-aarch64, osx-arm64, osx-64 and win-64. Bump `rev` and `build: number` together.

`colmap-metal` and `pycolmap-metal` (COLMAP with a Metal PatchMatch backend,
the owner's fork) are not intended for conda-forge.

## What is built where

| Platform | Runner | Packages |
|---|---|---|
| linux-64 | `ubuntu-latest` | everything (+ noarch `taglab`) |
| linux-aarch64 | `ubuntu-24.04-arm` | everything except taglab |
| osx-arm64 | `macos-latest` | everything + `colmap-metal`, `pycolmap-metal` |
| osx-64 | `macos-15-intel` | everything except taglab |
| win-64 | `windows-latest` (VS 2022) | everything except taglab |

"Everything" = `py4dgeo`, `qcustomplot`, `dxflib`, `cloudcompare`, `libcoraline`, `simsimd`,
`qhoptim` (+ `pixi-pack-app` where installers are built). A noarch package built in several jobs
is uploaded by the first; the others skip it. OpenMVS, vcglib and portable-file-dialogs are on
conda-forge ([staged-recipes#35410](https://github.com/conda-forge/staged-recipes/pull/35410), merged)
and no longer built here.

`.github/workflows/build.yml` runs on every push to `main`, on pull requests
and manually (Actions > build > Run workflow). It builds with
`pixi run build` (`rattler-build build --skip-existing all`, set up by `prefix-dev/setup-pixi`
from `pixi.toml`), so a package already on the channel
is not rebuilt (bump `build: number` in a recipe, or its version, to publish a
new one). Uploads happen only from `main`/manual runs, with
`rattler-build upload prefix --skip-existing`: existing files are never overwritten.
**Never delete a package from the channel.** A deleted file name is free again: the next run on
`main` rebuilds it (skip-existing finds nothing) and uploads a file with the same name but other
bytes, and every `pixi.lock` that has the old one fails with a hash mismatch (colmap and pycolmap
for osx-arm64 in November 2026: deleted between two runs, rebuilt by the next merge,
reef-metrics needed a new lock). To replace a package, bump `build: number`; to retire one, stop
building it and leave the file.
Built packages are also kept as workflow artifacts for 14 days.

## Using the channel

```bash
pixi workspace channel add --prepend https://prefix.dev/tobias-fischer/reefshape
pixi add cloudcompare
```

In `pixi.toml`: `channels = ["https://prefix.dev/tobias-fischer/reefshape", "conda-forge"]`.
(Use this URL, not the website's `/channels/@...` route.) Keep it **before** conda-forge: with strict
channel priority the packages of this channel then win over same-named conda-forge ones, e.g. the
variants of `simsimd` and `taglab` that conda-forge's noarch or unix-only builds would otherwise shadow.

## Publishing: trusted publishing, no secret

The workflow file `.github/workflows/build.yml` of this repository is a trusted
publisher of the channel (prefix.dev channel settings > Trusted Publishers:
GitHub user `Tobias-Fischer`, repository `reefshape-recipes`, workflow
`build.yml`). The build jobs have `permissions: id-token: write`, and
`rattler-build upload prefix` exchanges the job's GitHub OIDC token for upload
rights: there is no API key or secret to manage. Renaming the workflow file
breaks publishing. Each job uploads its packages as soon as it finishes; pull requests never upload.
Speed-ups from RoboStack (measured in RoboStack/robostack#154): up to 3 parallel builds on
Linux/macOS (`--parallel-builds`), Windows builds on `D:` with Defender real-time scanning off,
Spotlight off on macOS.

## Building locally

```bash
pixi run build -r recipes/cloudcompare -r recipes/dxflib -r recipes/qcustomplot --output-dir out
```

`pixi.toml` pins rattler-build (and `pixi.lock` its exact build) and holds the `build` and
`upload` tasks the workflow runs too, so a local build is the CI build: our channel before
conda-forge, `conda_build_config.yaml`, `--skip-existing all`.

`conda_build_config.yaml` is a snapshot of conda-forge's pinning (matching ABI
pins). The Metal recipes take their own variant files, see
the last steps of the workflow. Upload by hand:
`rattler-build auth login prefix.dev` once, then
`pixi run upload out tobias-fischer/reefshape` (skips files already there).

## Recipe notes

| Recipe | Notes |
|---|---|
| `py4dgeo` | M3C2 for point-cloud change |
| `cloudcompare` | 2.14 with M3C2 / LAS / E57 plugins |
| `colmap-metal`, `pycolmap-metal` | COLMAP `metal_` build, osx-arm64 only |
| `taglab` | TagLab (GPL-3.0), noarch, upstream tarball + patches; `smoke.py` starts it offscreen |
| `libcoraline` | TagLab's Refine border (Coraline graph cut, vendored Boykov-Kolmogorov max-flow, GPL-3.0), shared library loaded with ctypes |
| `qhoptim` | QHAdam/QHM optimizers (MIT, noarch; PyPI only), for TagLab's Train your network |
| `simsimd` | 6.5.16, the last release with a `simsimd` module (conda-forge's 7.x is the renamed NumKong without it, which breaks albucore/albumentations 2.0.8); TagLab depends on `simsimd <7` |

Recipes originate from `reef-metrics/packaging/conda-recipes`; this repository
is now their home. License of the recipes: BSD-3-Clause (the packaged software
keeps its own license).
