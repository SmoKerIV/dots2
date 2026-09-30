# File Ownership Map

Orbit is a source repository, not a copy of a home directory. The categories
below explain what a fresh deployment creates and what remains local.

## Authored Orbit Source

- `config/hypr/`, `config/noctalia/`, `config/quickshell/`, `config/gtk-*`,
  `config/kitty/`, `config/wezterm/`, and `config/zed/` contain Orbit policy,
  templates, and adapters. `config/noctalia/50-orbit-shell.toml` is the
  tracked Noctalia shell baseline (bar, dock, templates, disabled duplicates).
- `bin/`, `lib/`, `systemd/user/`, `desktop/`, `plymouth/`, and `assets/`
  contain Orbit scripts, services, launchers, the boot theme, and sound assets.
- `bootstrap/install-packages`, `bootstrap/takeover`, `bootstrap/deploy`,
  `bootstrap/verify`, `bootstrap/status`, `bootstrap/migrate`, and
  `bootstrap/install-cachyos` contain package installation,
  replacement/backup, deployment, validation, a read-only state report,
  adoption/rollback, and the one-shot CachyOS flow.

## Deployed Links And Seeds

`bootstrap/deploy` symlinks authored files into `~/.config`, `~/.local/bin`,
`~/.local/lib`, and `~/.config/systemd/user`. It copy-seeds selected mutable
files, including `~/.config/qt6ct/qt6ct.conf`, the `~/.config/hypr/monitors.lua`
placeholder, and the Orbit desktop entry, only when they do not already exist.
`bootstrap/takeover` backs up whatever stands in the way first, under
`~/.local/state/orbit/takeover/<timestamp>/`.

## Generated Outputs

- `~/.config/hypr/hyprqt6engine.conf` is generated/maintained as the HyprQt6
  Engine configuration output and should not be treated as machine discovery.
- `~/.config/wezterm/wezterm.lua` is the generated/deployed WezTerm output;
  its palette comes from Noctalia and Orbit supplies presentation settings.
- Noctalia generates Hyprland, GTK, Qt/KDE, WezTerm, Kitty, and wallpaper-palette
  outputs (`~/.config/orbit-wallpaper-engine/palette.lua`).
  `orbit-update-all-colors` creates Orbit semantic and presentation
  adapters from those outputs.
 - `~/.config/hypr/monitors.lua` is seeded as a placeholder and then generated
   by `nwg-displays` per machine.

Generated files may be regular files even when their templates or generators
are tracked here. Edit the tracked source or the owning application's template,
not a generated result.

## Machine-Local, Runtime, And Cache State

- `~/.config/orbit/machine/` contains host-specific Sunshine display settings.
- Monitor connectors, modes, positions, application state, secrets, and host
  identities remain outside Git.
- Wallpaper Engine status, FIFOs, lock backgrounds, systemd state, Noctalia
  state, logs, caches, test results, and Python bytecode are runtime data.
- Plugin source/build trees belong in the user cache; installed plugin `.so`
  files belong under `~/.local/share/hyprland/plugins/` and are not tracked.

## External Boundaries

Hyprland, Noctalia, QuickShell, all plugin source, and the Wallpaper Engine
source tree are independent projects. Orbit records their accepted revisions
and integration points, but does not copy their source into this repository.
The v0.1 Wallpaper Engine x86-64 ELF is the deliberate offline artifact
exception documented in [`external-components.md`](external-components.md).
