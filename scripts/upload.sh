#!/usr/bin/env bash
# Upload every package under $1 to anaconda.org/tobiasrobotics, skipping files
# that are already there (never overwrite). Needs ANACONDA_API_TOKEN.
# cloudcompare 2.14 is a beta: it goes to the `dev` label until the release.
set -euo pipefail
dir=${1:?directory with packages}
python3 -m pip install --quiet anaconda-client
# the same noarch package is built by several jobs: upload each file name once
declare -A seen
main=(); dev=()
while IFS= read -r f; do
  b=$(basename "$f")
  [ -n "${seen[$b]:-}" ] && continue
  seen[$b]=1
  case "$b" in cloudcompare-*) dev+=("$f");; *) main+=("$f");; esac
done < <(find "$dir" \( -name '*.conda' -o -name '*.tar.bz2' \) | sort)
echo "${#main[@]} package(s) for main, ${#dev[@]} for dev"
# the token is read from ANACONDA_API_TOKEN by the client; it is never printed
[ ${#main[@]} -gt 0 ] && anaconda upload --user tobiasrobotics --label main --skip-existing "${main[@]}"
[ ${#dev[@]} -gt 0 ] && anaconda upload --user tobiasrobotics --label dev --skip-existing "${dev[@]}"
exit 0
