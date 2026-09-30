# Optional Integrations

Optional integrations do not make their application a core Orbit dependency.
All of them use native pacman/CachyOS packages
(`bootstrap/install-packages --optional`); the Flatpak IDs remain only as
fallbacks inside the helpers.

- **Sunshine:** `bin/orbit-sunshine-display`, its watchdog unit, drop-ins for
  both the native `sunshine.service` and the Flatpak unit, and the
  machine-local display profile preserve save/switch/watchdog/restore behavior.
  Connector names, modes, resolutions, and host identities are never stored in
  the repository.
- **Game sessions:** `orbit-game-run`, `orbit-game-session.service`, and its
  timer integrate Steam/GameMode behavior.
- **Obsidian:** `configure-obsidian` installs the tracked appearance snippet into
  a vault selected by `OBSIDIAN_VAULT`.
- **Zen:** `configure-zen` installs the tracked browser chrome override into the
  active profile (`zen-browser-bin` from the CachyOS repository).
- **Zed:** the tracked theme and settings provide the supported presentation
  integration (`zeditor` is the Arch binary name).
- **Nautilus Actions:** the installer verifies and installs the pinned upstream
  extension; it needs `nautilus-python`.
- **LocalSend:** `localsend.service` runs the native `localsend` package
  through `show-localsend --daemon`; `configure-localsend` renames the device
  and `configure-localsend-firewall` opens port 53317 in `ufw` or `firewalld`.
- **GPU Screen Recorder:** `gpu-screen-recorder-control` drives the native
  `gpu-screen-recorder`/`gsr-cli`; `install-gpu-screen-recorder` installs it.
- **Mission Center:** `missioncenter` is the `CTRL+SHIFT+Escape` task manager.
- **Plymouth:** `install-plymouth-theme` installs the source theme with the
  CachyOS logo and rebuilds the initramfs; it is privileged and separate from
  deployment.
- **Noctalia Greeter:** available from the CachyOS repository for greetd users;
  `orbit-sync-noctalia-greeter` only acts when `greetd.service` is enabled, so
  SDDM installs are unaffected.
