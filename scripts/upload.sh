#!/usr/bin/env bash
# Upload every package under $1 to the prefix.dev channel $2 (e.g. tobias-fischer/reefshape),
# skipping files that are already there (never overwrite). In GitHub Actions
# rattler-build authenticates with the job's OIDC token (trusted publishing,
# needs `permissions: id-token: write`); no secret. Locally: `rattler-build auth login prefix.dev`.
set -euo pipefail
dir=${1:?directory with packages}; channel=${2:?channel}
# the same noarch package is built by several jobs: upload each file name once
declare -A seen
files=()
while IFS= read -r f; do
  b=$(basename "$f")
  [ -n "${seen[$b]:-}" ] && continue
  seen[$b]=1
  files+=("$f")
done < <(find "$dir" \( -name '*.conda' -o -name '*.tar.bz2' \) | sort)
echo "${#files[@]} package(s) to upload to $channel"
[ ${#files[@]} -eq 0 ] && exit 0
rattler-build upload prefix --channel "$channel" --skip-existing "${files[@]}"
