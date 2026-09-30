# Dependencies

Orbit is validated on CachyOS (Arch Linux) with Wayland, Hyprland `0.56.2`,
and Noctalia `5.2`. `bootstrap/install-packages` installs the groups below;
they are the intended dependency boundary, not an inventory of one machine.
Arch does not split `-devel` packages, so the runtime packages already provide
the headers the plugin builds need.

## Required Runtime (`install-packages --core`)

- `hyprland`, `hyprpm`, `hypridle`, `hyprlock`, `hyprpolkitagent`,
  `hyprpicker`, `hyprcursor`, `hyprtoolkit`, `noctalia`, and `quickshell`
  (all `[extra]`);
- `xdg-desktop-portal`, `xdg-desktop-portal-hyprland`,
  `xdg-desktop-portal-gtk`, and `polkit`;
- `nwg-displays` for the machine-local monitor layout;
- `python`, `python-pyudev`, `python-evdev`, `python-gobject`, `jq`, `socat`,
  `util-linux`, `shadow`, `procps-ng`, `dbus`, `grim`, `slurp`,
  `wl-clipboard`, `zenity`, `libcanberra`, and `alsa-utils`;
- `qt6ct`, `kitty`, `wezterm`, `nautilus`, `gnome-calculator`, `fastfetch`,
  `micro`, `ttf-jetbrains-mono`, `noto-fonts`, `noto-fonts-emoji`, and
  `adw-gtk-theme`.

These provide the commands used by the core launchers and user services,
including `systemctl`, `hyprctl`, `flock`, `sg`, `ps`, `wl-copy`, and
`canberra-gtk-play`. `sg input` additionally requires membership of the `input`
group, which `install-packages` grants.

## AUR (`install-packages --aur`, through `paru`)

- `hyprqt6engine` (Qt6 theme provider selected by `orbit-launch`);
- `kora-icon-theme` (the icon theme named in `config/hypr/appearance.toml`).

## Required External Projects

- Hyprland and Noctalia, which remain the compositor and shell/palette owners;
- QuickShell, which hosts Orbit's global-menu configuration;
- the four Hyprland plugins and the Oblique cursor theme listed in
  [`external-components.md`](external-components.md);
- the independent Orbit Wallpaper Engine project. v0.1 includes an x86-64
  runtime artifact, but its source and integration checkout remain external.

## Plugin Build Dependencies (`install-packages --build`)

- `base-devel`, `git`, `patch`, `pkgconf`, and `cmake`;
- the `hyprland` package itself, which installs `/usr/include/hyprland` and
  `/usr/share/pkgconfig/hyprland.pc` matching the installed compositor;
- `pixman`, `libdrm`, `pango`, `libinput`, `systemd-libs`, `wayland`,
  `libxkbcommon`, `lua` (5.4), `cairo`, `libpng`, `mesa`, and `libglvnd`.

Hyprland plugins are ABI-sensitive. Installers fail clearly when required
compiler or `pkg-config` dependencies are missing and warn when the running
Hyprland commit differs from the validated reference. Because the headers come
from the same package as the binary, `hyprpm update` is not needed.

## Optional Applications And Integrations (`install-packages --optional`)

- `mission-center` (task manager on `CTRL+SHIFT+Escape`), `gpu-screen-recorder`
  and `gpu-screen-recorder-ui`;
- `syncthing`, `gamemode`, and `steam` for game sessions;
- `obsidian`, `zed`, `nautilus-python` (Actions For Nautilus), and `plymouth`;
- from the CachyOS repository: `localsend`, `sunshine`, `zen-browser-bin`,
  and `chatgpt-desktop-bin`.

Optional installers and machine-local requirements are documented in
[`optional-integrations.md`](optional-integrations.md). They are not needed for
the core Orbit session. Flatpak is no longer required; the helpers fall back to
the Flatpak IDs only when a native package is absent.
