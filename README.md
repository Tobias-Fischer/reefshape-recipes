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
| `openmvs`, `vcglib`, `portable-file-dialogs` | [#35410](https://github.com/conda-forge/staged-recipes/pull/35410) |
| `py4dgeo` | [#35418](https://github.com/conda-forge/staged-recipes/pull/35418) |
| `cloudcompare` (+ `qcustomplot`, `dxflib`) | [#35422](https://github.com/conda-forge/staged-recipes/pull/35422) |
| `taglab` | [#35457](https://github.com/conda-forge/staged-recipes/pull/35457) |

`colmap-metal` and `pycolmap-metal` (COLMAP with a Metal PatchMatch backend,
the owner's fork) are not intended for conda-forge.

## What is built where

| Platform | Runner | Packages |
|---|---|---|
| linux-64 | `ubuntu-latest` | everything (+ noarch `taglab`) |
| linux-64 CUDA | `ubuntu-latest` | `openmvs` / `pyopenmvs` cuda12 and cuda13 (`CF_CUDA_ENABLED=True`, no GPU: tests do not run the GPU tools) |
| linux-aarch64 | `ubuntu-24.04-arm` | everything except taglab |
| osx-arm64 | `macos-latest` | everything + `colmap-metal`, `pycolmap-metal` |
| osx-64 | `macos-15-intel` | everything except taglab |
| win-64 | `windows-latest` (VS 2022) | everything except taglab |
| win-64 CUDA | `windows-latest` | `openmvs` / `pyopenmvs` CUDA |

"Everything" = `vcglib`, `portable-file-dialogs`, `openmvs` (+ `pyopenmvs`),
`py4dgeo`, `qcustomplot`, `dxflib`, `cloudcompare`. The noarch packages are
built in every job (OpenMVS needs them) and uploaded once.

`.github/workflows/build.yml` runs on every push to `main`, on pull requests
and manually (Actions > build > Run workflow). It builds with
`rattler-build build --skip-existing all`, so a package already on the channel
is not rebuilt (bump `build: number` in a recipe, or its version, to publish a
new one). Uploads happen only from `main`/manual runs, with
`rattler-build upload prefix --skip-existing`: existing files are never overwritten.
Built packages are also kept as workflow artifacts for 14 days.

## Using the channel

```bash
pixi workspace channel add --prepend https://prefix.dev/tobias-fischer/reefshape
pixi add openmvs
```

In `pixi.toml`: `channels = ["https://prefix.dev/tobias-fischer/reefshape", "conda-forge"]`.
(Use this URL, not the website's `/channels/@...` route.)

## Publishing: trusted publishing, no secret

The workflow file `.github/workflows/build.yml` of this repository is a trusted
publisher of the channel (prefix.dev channel settings > Trusted Publishers:
GitHub user `Tobias-Fischer`, repository `reefshape-recipes`, workflow
`build.yml`). The `upload` job has `permissions: id-token: write`, and
`rattler-build upload prefix` exchanges the job's GitHub OIDC token for upload
rights: there is no API key or secret to manage. Renaming the workflow file
breaks publishing. Pull requests never upload.

## Building locally

```bash
pixi exec rattler-build build -r recipes/openmvs -r recipes/vcglib -r recipes/portable-file-dialogs \
  --skip-existing local -c conda-forge -c https://prefix.dev/tobias-fischer/reefshape -m conda_build_config.yaml --output-dir out
```

`conda_build_config.yaml` is a snapshot of conda-forge's pinning (matching ABI
pins). CUDA variants: `CF_CUDA_ENABLED=True`, and on a machine without a GPU
`CONDA_OVERRIDE_CUDA=13.4`. The Metal recipes take their own variant files, see
the last steps of the workflow. Upload by hand:
`rattler-build auth login prefix.dev` once, then
`rattler-build upload prefix --channel tobias-fischer/reefshape --skip-existing out/*/*.conda`.

## Recipe notes

| Recipe | Notes |
|---|---|
| `openmvs` | OpenMVS 2.4.0 with patches (several backported from upstream, see comments in the recipe), cpu / cuda12 / cuda13, microarch levels on x86_64; outputs `openmvs` and `pyopenmvs` |
| `vcglib`, `portable-file-dialogs` | header-only build dependencies of OpenMVS, noarch |
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
