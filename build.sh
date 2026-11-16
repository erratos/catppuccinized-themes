#!/usr/bin/env bash
# Rebuild the themes and the release archives with catppuccinizer.
#
#   ./build.sh                 # uses `catppuccinize` from PATH
#   CATPPUCCINIZE=../catppuccinizer/catppuccinize ./build.sh
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
tool="${CATPPUCCINIZE:-catppuccinize}"

rm -rf themes dist
"$tool" plymouth hexa_retro infinite_seal -f mocha -a all -o themes
mkdir dist
for d in themes/*/; do
    n="$(basename "$d")"
    tar -C themes -czf "dist/$n.tar.gz" "$n"
done
echo "$(ls dist | wc -l) archives in dist/"
