# Deployment

`bootstrap/deploy` is intentionally small and idempotent.

It:

- creates required destination directories;
- symlinks authored Orbit configuration, scripts, libraries, QuickShell files,
  Noctalia drop-ins, and user units from this repository;
- seeds mutable Qt configuration, a `monitors.lua` placeholder, and the
  authored Wallpaper Engine desktop launcher only when the destination is
  absent;
- seeds the Orbit freedesktop sound theme only when its files are absent;
- enables core user services without starting or restarting the desktop;
- asks Noctalia to apply templates and runs the canonical Orbit appearance
  adapter path when Noctalia is running (otherwise the first session does it);
- refuses to replace an existing regular file or unrelated symlink.

`--list` prints the plan (`kind<TAB>source<TAB>destination`) without touching
anything; `--no-services` creates links and seeds only. The command does not
install packages, compile external plugins, modify monitor configuration, or
perform privileged operations. Use the dedicated documented install steps for
those tasks.

## Replacing an existing configuration

`bootstrap/takeover` is the explicit exception to deploy's refusal-only
behavior for a machine that already has a Hyprland/Noctalia configuration (the
CachyOS skeleton, end-4 dots, or anything else). It computes deploy's plan,
moves every conflicting destination plus known foreign Hyprland and Noctalia
files into `${XDG_STATE_HOME:-$HOME/.local/state}/orbit/takeover/<timestamp>/`,
writes a manifest, and then runs deploy. `--dry-run` only lists the moves,
`--reset-noctalia-state` also sets aside Noctalia's GUI overrides, and
`--restore DIR` removes Orbit's links, seeds, and empty directories, disables
its user units, and moves the files back. Restore refuses to overwrite a
destination that changed after the takeover.

## Adopting an Orbit-shaped home

`bootstrap/migrate --dry-run` previews the bounded adoption of files that are
already identical or known-portable. Its `--adopt` mode snapshots replaced
files and writes a manifest below
`${XDG_STATE_HOME:-$HOME/.local/state}/orbit/migrations/`; it never replaces
directories and blocks unexpected content. Rollback uses the printed manifest:

```sh
./bootstrap/migrate --rollback \
  "$HOME/.local/state/orbit/migrations/<timestamp>/manifest.json"
```

Rollback refuses to remove a destination that changed after adoption. Normal
deployment creates links and enables user units, but does not start or restart
the desktop. Start a fresh Hyprland session after deployment to load the
configuration and plugins; a reboot is normally unnecessary.

Plymouth installation (`bin/install-plymouth-theme`) requires privilege and is
a separate operation.

To deploy optional user services:

```sh
./bootstrap/deploy --optional
```

Sunshine display recovery additionally requires a machine-local file at
`~/.config/orbit/machine/sunshine-display.conf`, based on
`config/orbit/machine/sunshine-display.conf.example`.
