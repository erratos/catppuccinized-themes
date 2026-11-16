# catppuccinized-themes

Ready-to-use themes in [Catppuccin](https://catppuccin.com), made with
[catppuccinizer](https://github.com/erratos/catppuccinizer).

## Plymouth: hexa_retro and infinite_seal (Mocha)

Two boot animations by [adi1090x](https://github.com/adi1090x/plymouth-themes),
recoloured in Catppuccin Mocha.

| hexa_retro | infinite_seal (mauve) |
|:---:|:---:|
| ![hexa_retro](assets/hexa-retro.gif) | ![infinite_seal](assets/infinite-seal-mauve.gif) |
| `catppuccin-mocha-hexa-retro` | `catppuccin-mocha-infinite-seal-<accent>` |
| white → `text`, red → `red`, yellow → `yellow`, blue → `blue`, cyan → `teal` | white → accent |

infinite_seal comes in the 14 Mocha accents:

![accents](assets/infinite-seal-accents.png)

Every theme also has a `…-status` variant: a thin progress bar and the last
systemd services started, under the animation.

### Install

Download an archive from the [Releases](../../releases), then:

```bash
tar xf catppuccin-mocha-infinite-seal-mauve.tar.gz
sudo cp -r catppuccin-mocha-infinite-seal-mauve /usr/share/plymouth/themes/
sudo plymouth-set-default-theme -R catppuccin-mocha-infinite-seal-mauve
```

`-R` rebuilds the initramfs, needed for the theme to show at boot. On KDE you
can also pick it in *System Settings → Boot Splash Screen* once copied. Make
sure `splash` is on your kernel command line and the `plymouth` hook is in your
initramfs (`HOOKS=(… plymouth …)` in `/etc/mkinitcpio.conf`).

### Other flavours and accents

The releases contain Mocha. Any other combination takes one command with
catppuccinizer:

![flavours](assets/hexa-flavors.png)

```bash
catppuccinize plymouth hexa_retro -f latte
catppuccinize plymouth infinite_seal -f macchiato -a teal --install
```

## Rebuilding

```bash
./build.sh            # needs catppuccinizer: pipx install git+https://github.com/erratos/catppuccinizer.git
```

`build.sh` regenerates `themes/` and the archives in `dist/` that are attached
to the releases.

## Credits & licence

- Original animations: [Aditya Shakya (@adi1090x)](https://github.com/adi1090x/plymouth-themes), GPL-3.0.
- Colours: [Catppuccin](https://github.com/catppuccin/catppuccin).
- Released under the GPL-3.0, like the original themes. Not affiliated with
  the official [catppuccin/plymouth](https://github.com/catppuccin/plymouth) port.
