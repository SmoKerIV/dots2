# Installation

This is the canonical Orbit v0.1 installation path for CachyOS (Arch Linux).
It assumes the CachyOS Hyprland edition or any CachyOS/Arch install with
Hyprland available from the official repositories. Commands below are run from
the Orbit checkout unless stated otherwise.

## Quick path

```sh
git clone https://github.com/CleanShirtUK/dotfiles.git ~/src/orbit-dotfiles
cd ~/src/orbit-dotfiles
./bootstrap/install-cachyos            # add --optional for Steam/Sunshine/LocalSend/etc.
```

`install-cachyos` runs the steps below in order and stops at the first
failure; each step is idempotent and can be rerun on its own. Add
`--reset-noctalia-state` to also set aside Noctalia's GUI overrides so the
tracked Orbit shell layout is what you see, and `--yes` to skip the takeover
confirmation.

Afterwards log out, choose the **Hyprland** session in SDDM (not the
UWSM-managed entry), and run `nwg-displays` once.

## 1. Install Packages

```sh
./bootstrap/install-packages              # core + build toolchain + AUR (paru)
./bootstrap/install-packages --optional   # applications Orbit integrates with
./bootstrap/install-packages --all --dry-run
```

Everything with an official package comes from `[extra]`/`[core]`; the
CachyOS repository supplies the AUR-derived applications (`localsend`,
`sunshine`, `zen-browser-bin`, `chatgpt-desktop-bin`) as normal pacman
packages, and `paru` (shipped with CachyOS) installs the two AUR packages
(`hyprqt6engine`, `kora-icon-theme`). The script also adds your user to the
`input` group, which `workspace-alt-tab-input.service` needs; that takes effect
at the next login. The package groups are listed in
[`dependencies.md`](dependencies.md).

## 2. Replace The Existing Configuration

A fresh CachyOS Hyprland install ships `cachyos-hypr-noctalia`, which places
`~/.config/hypr/hyprland.lua`, `~/.config/hypr/config/*.lua`,
`~/.config/noctalia/config.toml`, `kitty.conf`, GTK CSS, and `qt6ct.conf` in
the home directory. `bootstrap/deploy` refuses to overwrite any of them, so:

```sh
./bootstrap/takeover --dry-run   # list what would be moved
./bootstrap/takeover             # back up, then deploy
```

Takeover moves every conflicting file into
`~/.local/state/orbit/takeover/<timestamp>/`, writes a manifest, and runs
`bootstrap/deploy`. Nothing is deleted. It also sets aside foreign Hyprland
modules (`hypr/config`, `hypr/custom`, `hyprland.conf`, …) and other Noctalia
drop-ins that would otherwise load next to Orbit's files. Undo with:

```sh
./bootstrap/takeover --restore ~/.local/state/orbit/takeover/<timestamp>
```

Deploy itself creates Orbit-owned symlinks under `~/.config`, `~/.local/bin`,
`~/.local/lib`, and `~/.config/systemd/user`; seeds copy-once files
(`qt6ct.conf`, a `monitors.lua` placeholder, the desktop entry); enables core
user units; and refreshes Noctalia templates when Noctalia is running. Use
`./bootstrap/deploy --optional` to also enable the game-session and LocalSend
units, and `--list` to print the plan.

For a home that is already Orbit-shaped (a previous machine), the bounded
`bootstrap/migrate --dry-run` / `--adopt` / `--rollback` flow remains available.

## 3. Build External Components

Arch's `hyprland` package installs the compositor headers and `hyprland.pc`, so
the plugins build against exactly the running ABI without `hyprpm update`:

```sh
./bin/install-hyprglass
./bin/install-scrolloverview
./bin/install-hyprwindowshade
./bin/install-dynamic-cursors
./bin/install-oblique-cursor
```

The installers use pinned upstream commits, build under the user cache, and
install only the resulting `.so` files to `~/.local/share/hyprland/plugins/`
(the cursor theme goes to `~/.local/share/icons/oblique-cursor`). They do not
load anything into the running compositor. The accepted reference for all
plugins is Hyprland `0.56.2` at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`; rebuild after a Hyprland update.

Wallpaper Engine is a separate project:

```sh
./bin/dotfiles-install-wallpaper
```

This clones the pinned `v0.2.0` tag over HTTPS into
`~/.local/src/orbit-wallpaper-engine`, builds it, installs its Noctalia
integration and settings tool, and enables the user service. The runtime used
by the service is the tracked x86-64 artifact described in
[`external-components.md`](external-components.md).

## 4. Configure This Machine

Monitor layout is intentionally machine-local:

```sh
nwg-displays
```

It overwrites the seeded `~/.config/hypr/monitors.lua`; Orbit discovers
connected monitors at runtime for semantic workspace behavior and the
`SUPER+1/2/3` monitor binds. Noctalia is the source of truth for colors; do not
edit generated color outputs as if they were Orbit inputs.

The tracked Noctalia shell layout
([`config/noctalia/50-orbit-shell.toml`](../config/noctalia/50-orbit-shell.toml))
is a starter. GUI changes land in `~/.local/state/noctalia/settings.toml` and
win over it. To carry an exact look from another Orbit machine, run
`noctalia config export` there and replace the tracked file.

Optional, privileged extras:

- `./bin/install-plymouth-theme` installs the Orbit boot theme with the
  CachyOS logo and rebuilds the initramfs (`plymouth-set-default-theme -R`).
- `./bin/configure-localsend-firewall` opens the LocalSend port in `ufw`
  (CachyOS default) or `firewalld`.
- Sunshine needs a machine-local profile copied from
  `config/orbit/machine/sunshine-display.conf.example`.

The display manager is left alone. Orbit is validated with SDDM launching the
plain `hyprland.desktop` session. Noctalia Greeter (CachyOS repo package) is
optional; the greeter background sync only runs when `greetd` is enabled.

## 5. Verify And Start Using Orbit

```sh
./bootstrap/verify
./tests/orbit/run-all
```

Log out and start a new Hyprland session after deployment so the authored
configuration and newly installed plugins are loaded. Live tests require an
active non-root Hyprland session. Keybindings are listed in
[`keybinds.md`](keybinds.md).

## Rollback

- Takeover: `./bootstrap/takeover --restore ~/.local/state/orbit/takeover/<timestamp>`
  removes Orbit's links, seeds, and empty directories, disables its user units,
  and moves the backed-up files back. It refuses to overwrite anything that
  changed after the takeover.
- Adoption manifests: `./bootstrap/migrate --rollback "$HOME/.local/state/orbit/migrations/<timestamp>/manifest.json"`.

Reverting the Orbit Git checkout is separate from restoring machine-local state
and generated outputs.
