#!/bin/sh
# Metal pycolmap (osx-arm64), against the colmap metal_ build on tobiasrobotics
cd "$(dirname "$0")"
pixi exec rattler-build build -r recipe.yaml -m variant.yaml -m python.yaml -c tobiasrobotics -c conda-forge --output-dir out
