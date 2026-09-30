# External Components

Orbit owns its configuration, session coordination, launcher routing, and
deployment logic. The compositor, shell, plugins, and Wallpaper Engine listed
here remain independent components. Do not commit their source checkouts or
compiled plugin `.so` files to this repository.

## Reference Environment

The accepted reference environment uses CachyOS (Arch Linux) packages:

```text
Hyprland 0.56.2-3 (extra)
Hyprland commit efb50993780079460b0cbed1363e2166a2de1d9f
Noctalia 5.2.0-1 (extra)
QuickShell 0.3.1-1 (extra)
```

The Hyprland commit is identical to the original Fedora 44 reference
(`0.56.2-1.fc44`), so the pinned plugin revisions carry over unchanged. Arch's
`hyprland` package installs the matching headers and `hyprland.pc`; the
installers build against them directly and never need `hyprpm update`.

Hyprland plugins use private compositor APIs and must be rebuilt when the
Hyprland ABI or relevant dependency ABI changes. The running compositor loads
plugins from `~/.local/share/hyprland/plugins/` through the authored
`config/hypr/hyprland.lua` startup path.

## Hyprland Plugins

| Component | Upstream and revision | Current installation | Build/rebuild procedure | Coupling |
|---|---|---|---|---|
| Hyprglass | `https://github.com/hyprnux/hyprglass.git` at `5bc835dcc909cef6980291688143048cf16942b5` | `~/.local/share/hyprland/plugins/hyprglass.so` | Run `bin/install-hyprglass`; it fetches and verifies the pinned commit in the cache, runs the upstream `make`, and installs `hyprglass.so` | Build against the installed Hyprland ABI; the installer warns when the running compositor differs from the validated reference |
| ScrollOverview | `https://github.com/yayuuu/hyprland-scroll-overview.git` at `f9248ab6bee770e9d68813b48cc6ca12b3271254` | `~/.local/share/hyprland/plugins/libscrolloverview.so` | Run `bin/install-scrolloverview`; it fetches and verifies the pinned commit in the cache, runs the upstream production `make all`, and installs it as `libscrolloverview.so` | Plugin API is Hyprland-version-sensitive; the installer warns when the running compositor differs from the validated reference; upstream's `new-release` branch is not used |
| HyprWindowShade | `https://github.com/ManofJELLO/HyprWindowShade.git` at `40b756befa36cfd5cbed65d554c719141a65c420` | `~/.local/share/hyprland/plugins/HyprWindowShade.so` | Run `bin/install-hyprwindowshade`; it fetches the pinned commit, applies `config/hypr/patches/hyprwindowshade-per-window-effects.patch`, and compiles with `pkg-config hyprland` include flags (falling back to `/var/cache/hyprpm/$USER/headersRoot` where a distribution ships no headers) | Requires Hyprland 0.56-compatible headers and the running compositor commit; the patch is Orbit-owned |
| Dynamic Cursors | `https://github.com/virtcode/hypr-dynamic-cursors.git` at `5a224284872208b5324759d535d65061043725de` (`origin/v0.56.2`) | `~/.local/share/hyprland/plugins/dynamic-cursors.so` | Run `bin/install-dynamic-cursors`; it checks out the pinned revision, runs `make all`, and installs `out/dynamic-cursors.so` | x86-64 function-hook plugin; rebuild for the installed Hyprland ABI |
| Oblique Cursor | `https://github.com/kayxean/oblique-cursor.git` at `ecddc552b8a5eb53fbf7498f0e60fbd634906b4a` | `~/.local/share/icons/oblique-cursor` | Run `bin/install-oblique-cursor`; it copies the prebuilt `dist/theme_oblique-cursor` (or builds it with `hyprcursor-util`) | hyprcursor theme selected through `HYPRCURSOR_THEME`; not ABI-sensitive |

The installers keep source and build trees under
`$XDG_CACHE_HOME/orbit-hyprland-plugins` (or `$HOME/.cache/...`) and install
only the resulting `.so` files under `~/.local/share/hyprland/plugins/`. They
are safe to rerun, verify detached HEAD against the accepted revision, and do
not enable or reload plugins in the running compositor. The accepted validation
reference is Hyprland `0.56.2` at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, so compatibility beyond that ABI
has not been established.

### HyprWindowShade Patch

The local patch adds the address-targeted shader API, event-relative
`effect_time`, and a render-surface fallback used by
`config/hypr/scripts/window-shader-events`. It must be applied after checking
out the upstream revision and before compiling. The installer keeps the build
checkout under the cache and installs only the resulting `.so` outside Git.

## Orbit Wallpaper Engine

The independent project is:

```text
https://github.com/CleanShirtUK/orbit-wallpaper-engine.git
tag: v0.2.0
commit: dfbf5e24a42b6bf2af586b8286e2648dbb2b7420
```

The local checkout is maintained at `~/.local/src/orbit-wallpaper-engine` with
only the intended `origin` remote. Its `Makefile` builds the C renderer from
the checked-in Wayland protocol bindings and installs the renderer, control
tools, settings UI, desktop file, shaders, and user service. The external
project's `v0.2.0` tag is the accepted release corresponding to the current
runtime.

For Orbit's accepted integration, use:

```sh
bin/dotfiles-install-wallpaper
```

The wrapper defaults to `v0.2.0` (override with `ORBIT_WALLPAPER_REF` only for
an intentional update) and to the public HTTPS remote (override with
`ORBIT_WALLPAPER_REPO_URL`), fetches and checks out that ref, runs `make`, and
installs the external settings tool and Noctalia integration. The authored
Orbit desktop launcher and routing wrapper are deployed from this repository by
`bootstrap/deploy`. The wrapper does not change the external source ownership
or copy its source into Orbit.

## Wallpaper Engine ELF Exception

`bin/orbit-wallpaper-engine` is a 64-bit x86-64 Linux ELF, SHA-256
`7a4c8cfb58e7b995366dea48233f661323d40fe2f7dc891d39b8ce93ff36ae42`.
`systemd/user/orbit-wallpaper-engine.service` consumes it through
`~/.local/bin/orbit-wallpaper-engine`, and `bootstrap/deploy` links that path
to the repository file. It is deliberately retained so a fresh clone can
prepare the accepted renderer deployment without requiring a compiler or an
external checkout first. It links only against `libwayland-client`,
`libwayland-egl`, `libEGL`, `libGLESv2`, `libpng16`, `libffi`, and glibc, all
of which the CachyOS `hyprland` dependency set already provides.

The ELF is not an external source checkout or a Hyprland plugin. It is a
host-architecture-specific offline runtime artifact built from the independent
Wallpaper Engine project. The external project's Makefile is the authoritative
source/build procedure for updates; after an intentional renderer update, the
vendored artifact must be replaced and its hash re-recorded. It is not
portable to non-x86-64 systems and is not claimed to be bit-for-bit
reproducible from the recorded compiler alone.

## Noctalia Wallpaper Integration

The external project owns and supplies:

- `integrations/noctalia/plugin.toml` and `widget.luau`;
- `tools/orbit-wallpaper-settings`;
- the standalone settings QML payload;
- the external project's integration metadata.

`bin/dotfiles-install-wallpaper` installs those artifacts from the pinned
external checkout. Orbit owns and supplies:

- `bin/orbit-wallpaper-launcher`;
- `desktop/orbit-wallpaper-engine-settings.desktop`;
- the installer and deployment/verification checks;
- the Hyprland top-right placement and single-window routing behavior.

The external Noctalia widget remains a separate visible widget action. The
authored desktop entry gives the generic Noctalia application launcher the
same Orbit routing behavior without duplicating the renderer or service.

## Other External Dependencies

Noctalia, QuickShell, Hyprland, Hypridle, Hyprlock, and the Hyprland headers
are installed pacman packages rather than source owned by Orbit. GPU Screen
Recorder, LocalSend, Mission Center, Sunshine, Actions For Nautilus, Steam,
and application integrations are package-based optional components documented
in `docs/dependencies.md` and `docs/optional-integrations.md`; they are not
tracked build outputs here.

## Update Procedure

1. Check the upstream release and compatibility notes against the installed
   Hyprland version.
2. Update the relevant revision, build instructions, and artifact location in
   this document before rebuilding.
3. Rebuild outside the repository and install the resulting artifact outside
   Git.
4. Load/test the plugin in a controlled session, then run Orbit source and
   live verification.
5. For Wallpaper Engine, update the external checkout/tag and the vendored
   ELF hash together; do not copy the external source tree into Orbit.
