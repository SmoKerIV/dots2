# Orbit

Orbit is an early-release (`v0.1`) CachyOS + Hyprland desktop configuration.
It provides authored Hyprland policy, session services, application routing,
workspace behavior, a QuickShell global menu, and integration with Noctalia and
the independent Orbit Wallpaper Engine. It began life on Fedora 44 and was
ported to CachyOS (Arch Linux); the keybindings are the CachyOS Hyprland
defaults so a fresh CachyOS install keeps its original binds.

Orbit does not replace Hyprland or Noctalia. Hyprland remains the compositor;
Noctalia remains the shell and color-palette authority. Orbit owns the glue
between them and its own user services. External plugin source and compiled
plugins are installed outside this repository.

## Validated Platform

The supported reference is CachyOS (rolling, Arch-based) with Wayland and:

- Hyprland `0.56.2-3` (extra), commit `efb50993780079460b0cbed1363e2166a2de1d9f`;
- Noctalia `5.2.0` (extra);
- QuickShell `0.3.1` (extra);
- an x86-64 system for the v0.1 Wallpaper Engine artifact.

The same Hyprland commit was the Fedora 44 reference, so the pinned plugins
build unchanged. Compatibility beyond this reference is not promised. Hyprland
plugins use private compositor APIs and may need rebuilding after Hyprland or
ABI-related dependency updates.

## Features

- Noctalia-driven colors with Orbit adapters for GTK, Qt/KDE, Kitty, WezTerm,
  Hyprland, and Hyprlock;
- Hyprland workspace policy, application placement, Alt+Tab, transitions, and
  lock/session services;
- CachyOS default keybindings ([`docs/keybinds.md`](docs/keybinds.md));
- QuickShell global menu and Orbit-routed Wallpaper Engine settings;
- Hyprglass, ScrollOverview, HyprWindowShade, and Dynamic Cursors integration;
- optional Sunshine, game-session, Nautilus, LocalSend, recorder, browser,
  editor, and Plymouth integrations, all from native pacman/CachyOS packages.

## Install

On a fresh CachyOS Hyprland install, one command does everything:

```sh
git clone https://github.com/CleanShirtUK/dotfiles.git ~/src/orbit-dotfiles
cd ~/src/orbit-dotfiles
./bootstrap/install-cachyos
```

It installs the packages, backs up and replaces the CachyOS default
configuration (`bootstrap/takeover`), deploys Orbit, builds the pinned plugins,
installs the cursor theme and Wallpaper Engine, and verifies the result. The
step-by-step version, and how to undo it, is in
[`docs/install.md`](docs/install.md). It does not change the display manager
(SDDM stays), monitor layout, or Plymouth.

Deployment is refusal-oriented: `bootstrap/deploy` will not overwrite unrelated
files. `bootstrap/takeover` is the explicit exception that moves conflicting
files into a restorable backup first. Neither installs packages or performs
privileged operations; `bootstrap/install-packages` handles pacman/paru.

## Architecture

```text
Hyprland -> Noctalia + QuickShell global menu
         -> hyprland-session.target
              -> Wallpaper Engine, workspace, shader, idle, and policy services

Noctalia palette/templates -> Orbit semantic and presentation adapters
Orbit configuration       -> Hyprland policy, routing, and machine-independent services
Machine-local setup       -> nwg-displays monitor layout and optional Sunshine profile
```

See [`docs/architecture.md`](docs/architecture.md) and
[`docs/file-map.md`](docs/file-map.md) for ownership boundaries.

## Dependencies

Required packages, external projects, build requirements, and optional
integrations are separated in [`docs/dependencies.md`](docs/dependencies.md).
The plugin and Wallpaper Engine provenance is recorded in
[`docs/external-components.md`](docs/external-components.md).

## Verify, Recover, Update

After installation:

```sh
./bootstrap/verify
./tests/orbit/run-all
```

Live tests require an active non-root Hyprland session. `bootstrap/takeover
--dry-run` previews what a takeover would move; `bootstrap/takeover --restore
BACKUP_DIR` puts the previous configuration back and removes Orbit's links.
For an existing Orbit-compatible home, `bootstrap/migrate --dry-run` previews
bounded adoption instead; `--adopt` records a manifest and `--rollback` restores
it. See [`docs/deployment.md`](docs/deployment.md) for recovery and update
details.

## Limitations

See [`docs/known-issues.md`](docs/known-issues.md) for the short v0.1 list.
The most important limitations are the validated Hyprland ABI boundary, the
x86-64 Wallpaper Engine artifact, machine-local monitor/Sunshine setup, the
starter Noctalia shell layout, and known logout visual-parity follow-up work.

## Project Status

Orbit v0.1 is an early release. Updates should first be validated against the
reference platform and documented external revisions. Contributions and issue
reports should include the Hyprland version/commit, relevant plugin revisions,
and whether the issue reproduces without optional integrations.
