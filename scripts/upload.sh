#!/usr/bin/env bash
# Upload every package under $1 to the prefix.dev channel $2 (e.g. tobias-fischer/reefshape),
# skipping files that are already there (also when another job uploaded the same noarch file) (never overwrite). In GitHub Actions
# rattler-build authenticates with the job's OIDC token (trusted publishing,
# needs `permissions: id-token: write`); no secret. Locally: `rattler-build auth login prefix.dev`.
set -euo pipefail
dir=${1:?directory with packages}; channel=${2:?channel}
files=()
while IFS= read -r f; do files+=("$f"); done < <(find "$dir" \( -name '*.conda' -o -name '*.tar.bz2' \) | sort)
echo "${#files[@]} package(s) to upload to $channel"
[ ${#files[@]} -eq 0 ] && exit 0
rattler-build upload prefix --channel "$channel" --skip-existing "${files[@]}"
