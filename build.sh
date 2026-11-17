#!/usr/bin/env bash
# Rebuild the themes and the release archives with catppuccinizer.
#
#   ./build.sh                       # every type
#   ./build.sh ksplash limine        # only some: plymouth ksplash limine wallpapers
#   CATPPUCCINIZE=../catppuccinizer/catppuccinize ./build.sh
#
# Output: themes/<type>/<theme>/ and dist/<type>-<theme>.tar.gz (attached to
# the releases); the wallpapers themselves go to wallpapers/ (tracked in git).
#
# KDE splash screens and wallpapers are recoloured from packages that must be
# installed on the machine that builds them (listed in each type's README).
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
tool="${CATPPUCCINIZE:-catppuccinize}"
cachy_walls=/usr/share/wallpapers/cachyos-wallpapers
cachy_hello=/usr/share/icons/hicolor/scalable/apps/org.cachyos.hello.svg

plymouth() {
    "$tool" plymouth hexa_retro infinite_seal -f mocha -a all -o themes/plymouth
}

ksplash() {
    local o=themes/ksplash
    "$tool" ksplash org.kde.breeze.desktop -a mauve -o $o
    "$tool" ksplash CachyOS-Nord -a mauve -o $o
    "$tool" ksplash a2n.kuro -a mauve -o $o
    "$tool" ksplash MatrixKDEGlow -a mauve -o $o                       # green rain kept
    "$tool" ksplash MatrixKDEGlow -a lavender -m green=accent -o $o    # lavender rain
    "$tool" ksplash Weaving-Helix-Ring-Dark -a mauve lavender -o $o
}

limine() {
    "$tool" limine -a mauve lavender --wallpaper "$cachy_walls/limine-splash.png" \
        --method lut -o themes/limine
}

wallpapers() {
    local o=wallpapers
    "$tool" image "$cachy_walls/Cachy_Topography.jpg" -f macchiato -o $o
    "$tool" image "$cachy_hello" -o $o -s mauve-lavender-mauve \
        -m cyan=mauve blue=lavender cyan-2=lavender cyan-3=mauve
    "$tool" image "$cachy_hello" -o $o -s lavender-mauve-lavender \
        -m cyan=lavender blue=mauve cyan-2=mauve cyan-3=lavender
    "$tool" image "$cachy_hello" -o $o -s blue-sapphire-blue \
        -m cyan=blue blue=sapphire cyan-2=sapphire cyan-3=blue
    "$tool" image "$cachy_hello" -o $o -s teal-sky-teal \
        -m cyan=teal blue=sky cyan-2=sky cyan-3=teal
}

types=("$@")
[ ${#types[@]} -eq 0 ] && types=(plymouth ksplash limine wallpapers)
mkdir -p dist
for t in "${types[@]}"; do
    case $t in
        plymouth|ksplash|limine) ;;
        wallpapers) wallpapers; continue ;;
        *) echo "unknown type: $t" >&2; exit 1 ;;
    esac
    rm -rf "themes/$t" dist/"$t"-*.tar.gz
    "$t"
    for d in themes/"$t"/*/; do
        n="$(basename "$d")"
        tar -C "themes/$t" -czf "dist/$t-${n#"$t-"}.tar.gz" "$n"
    done
done
echo "$(ls dist | wc -l) archives in dist/"
