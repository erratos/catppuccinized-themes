# Limine boot menu

[← All themes](../README.md)

Catppuccin Mocha colours for the [Limine](https://github.com/limine-bootloader/limine)
boot menu, with the CachyOS Limine wallpaper recoloured. Two accents: `mauve`
and `lavender` (the colour of the branding line and the highlighted help keys).

![wallpaper](assets/wallpaper.png)

![menu colours](assets/colours.png)

## Install

Download `limine-catppuccin-mocha-<accent>.tar.gz` from the
[Releases](https://github.com/erratos/catppuccinized-themes/releases). It contains `limine-theme.conf` and
`wallpaper-mocha-<accent>.png`.

1. Copy the wallpaper to your ESP (where `limine.conf` lives, often `/boot`):

   ```bash
   tar xf limine-catppuccin-mocha-mauve.tar.gz
   sudo mkdir -p /boot/catppuccin
   sudo cp limine-catppuccin-mocha-mauve/wallpaper-mocha-mauve.png /boot/catppuccin/
   ```

2. Back up `limine.conf`, then paste the content of `limine-theme.conf` before
   the first menu entry (the first line starting with `/`). Comment out any
   global option it repeats (`wallpaper:`, `backdrop:`, `term_*`…).

3. If config enrollment is enabled, run `sudo limine-enroll-config`.

The snippet for mauve:

```
wallpaper: boot():/catppuccin/wallpaper-mocha-mauve.png
wallpaper_style: stretched
backdrop: 1e1e2e
term_palette: 45475a;f38ba8;a6e3a1;f9e2af;89b4fa;f5c2e7;94e2d5;bac2de
term_palette_bright: 585b70;f38ba8;a6e3a1;f9e2af;89b4fa;f5c2e7;94e2d5;a6adc8
term_background: 331e1e2e
term_foreground: cdd6f4
term_background_bright: 313244
term_foreground_bright: cdd6f4
interface_branding_colour: cba6f7
interface_help_colour: a6adc8
interface_help_colour_bright: cba6f7
```

## Automatic install, other flavours and accents

[catppuccinizer](https://github.com/erratos/catppuccinizer) does all of the above,
backs up `limine.conf`, and can undo it:

```bash
sudo catppuccinize limine -a mauve --recolor-wallpaper --apply   # recolours your current wallpaper
sudo catppuccinize limine --remove
```

## Credits

Wallpaper: `limine-splash.png` from [cachyos-wallpapers](https://github.com/cachyos/cachyos-wallpapers) (GPL-1.0).
