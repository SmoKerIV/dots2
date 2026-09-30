# Known Limitations

These are current, non-blocking v0.1 limitations rather than resolved defects.

- Orbit is validated against CachyOS with Hyprland `0.56.2` at commit
  `efb50993780079460b0cbed1363e2166a2de1d9f` and Noctalia `5.2`. Hyprland
  plugins may need to be rebuilt after compositor or relevant dependency ABI
  changes; CachyOS is rolling, so check `hyprctl version` after updates.
- Orbit is validated with the plain `hyprland.desktop` session started by SDDM.
  The UWSM-managed session entry is untested; `launchPrefix` in
  `config/hypr/hyprland.lua` exists for it but the session bootstrap assumes
  Hyprland starts Noctalia itself.
- The tracked Noctalia shell layout (`config/noctalia/50-orbit-shell.toml`) is a
  starter, not the exact layout of the original Fedora machine, whose GUI
  settings were never tracked. Export them with `noctalia config export` on a
  reference machine to carry the look across.
- The v0.1 Wallpaper Engine deployment artifact is x86-64 Linux only.
- Monitor layout is generated per machine by `nwg-displays`; Sunshine also
  requires a machine-local display profile and has not been validated across
  multiple hardware profiles.
- `orbit-game-run` and `orbit-game-session.service` expect a
  `~/.local/libexec/orbit-game-session` reconciler that is not tracked here.
- `orbit-daily-note` and `orbit-scratchpad` reference a
  `~/.config/wezterm/orbit-notes.lua` profile that is not tracked here.
- Logout and lock currently have different visual choreography. Matching them
  exactly is a post-v0.1 fast follow and does not block the release.
- Plymouth is optional; `bin/install-plymouth-theme` performs the privileged
  initramfs step and is not part of standard deployment.
- Optional application integrations are only active when their applications
  and machine-specific configuration are present.
