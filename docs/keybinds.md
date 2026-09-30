# Keybinds

Orbit uses the CachyOS Hyprland keybinds (`cachyos-hypr-noctalia`,
`/etc/skel/.config/hypr/config/binds.lua`) so a fresh CachyOS install keeps
its original bindings. Where Orbit already had a richer implementation of the
same action, the CachyOS key runs the Orbit helper. Orbit-only actions sit on
keys the CachyOS layout leaves free. `SUPER` is the main modifier.

Number keys are bound by physical keycode (`code:10`–`code:19`) so the layout
also works on AZERTY.

## Windows

| Key | Action | Implementation |
|---|---|---|
| `SUPER + Q` | Close window | Hyprland |
| `SUPER + Escape` | Click-to-kill | `hyprctl kill` |
| `SUPER + ALT + Space` | Toggle floating | Hyprland |
| `SUPER + D` | Maximize (fullscreen mode 1) | Hyprland |
| `SUPER + F` | Fullscreen | Hyprland |
| `SUPER + J` | Toggle split (dwindle only) | Hyprland |
| `SUPER + Arrow` | Focus in direction, crossing monitor edges and the workspace hierarchy | Orbit `focus-directional` |
| `SUPER + SHIFT + Arrow` | Move window in direction, across monitors and workspace edges | Orbit `move-window-workspace` |
| `ALT + Tab` | Workspace-oriented window switcher (ScrollOverview) | Orbit `workspace-alt-tab` |
| `SUPER + Tab` | Noctalia window switcher | `noctalia msg window-switcher` |
| `SUPER + SHIFT + 1/2/3` | Move window to monitor 1/2/3 (left→right order) | Orbit, runtime monitor list |
| `SUPER + SHIFT + Scroll` | Move window to previous/next monitor | Hyprland |
| `SUPER + CTRL + SHIFT + Left/Right` | Move window to previous/next workspace on this monitor | Hyprland |
| `SUPER + CTRL + SHIFT + Scroll` | Same, with the wheel | Hyprland |
| `SUPER + SHIFT + CTRL + 1..5` | Move window to workspace N on this monitor | Hyprland |
| `SUPER + SHIFT + ALT + 1..5` | Move window to workspace N silently | Hyprland |
| `SUPER + Left-drag` | Move window | Hyprland |
| `SUPER + Right-drag` | Resize window | Hyprland |
| Double-click | Toggle float/tile of the clicked window | Orbit `toggle-float-double-click` |
| `SUPER + Minus / Plus`, `SUPER + KP -/+` | Cursor zoom out / in | Hyprland |

## Launchers

| Key | Action | Command |
|---|---|---|
| `SUPER + Return` | Terminal | `wezterm` |
| `SUPER + E` | File manager | `nautilus` |
| `SUPER + T` | Editor | `zeditor` (Zed) |
| `SUPER + C`, `XF86Calculator` | Calculator | `gnome-calculator` |
| `SUPER + W` | Browser | `zen-browser` |
| `CTRL + SHIFT + Escape` | Task manager | `missioncenter` |
| `SUPER + Space` | Application launcher | Noctalia |
| `SUPER + .` | Emoji picker | Noctalia launcher `/emo` |
| `SUPER + Z` | Noctalia settings | Noctalia |
| `SUPER + X` | Control center | Noctalia |
| `SUPER + A` | Notifications | Noctalia control center |
| `SUPER + V` | Clipboard history | Noctalia |
| `SUPER + L` | Lock (Orbit choreography → Hyprlock) | Orbit `animate-lock` |
| `SUPER + ALT + C` | Session panel | Noctalia |
| `SUPER + M` | Confirmed logout with exit choreography | Orbit `animate-shutdown` |
| `SUPER + ALT + A` | ChatGPT | `chatgpt` |
| `SUPER + ALT + S` | OpenCode in a dedicated terminal | Orbit |
| `SUPER + ALT + D` | Today's daily note | Orbit `orbit-daily-note` |
| `SUPER + SHIFT + D` | Scratchpad note | Orbit `orbit-scratchpad` |

## Capture and theming

| Key | Action | Command |
|---|---|---|
| `Print` | Region screenshot | `noctalia msg screenshot-region` |
| `SUPER + Print` | Full-screen screenshot | `noctalia msg screenshot-fullscreen` |
| `SUPER + P` | Color picker | `hyprpicker -a -n` |
| `SUPER + SHIFT + R` | Start/stop recording | Orbit `gpu-screen-recorder-control record` |
| `SUPER + SHIFT + Z` | Save instant replay | Orbit `gpu-screen-recorder-control replay` |
| `SUPER + SHIFT + W` | Wallpaper Engine settings | Orbit `orbit-wallpaper-launcher` |

## Workspaces and monitors

| Key | Action |
|---|---|
| `SUPER + 1/2/3` | Focus monitor 1/2/3 (sorted left→right, top→bottom, like `orbit-home-workspaces`) |
| `SUPER + ALT + 1..5` | Focus workspace 1..5 (absolute) |
| `SUPER + CTRL + 1..5` | Focus workspace N on this monitor |
| `SUPER + CTRL + Left/Right` | Previous/next workspace on this monitor |
| `SUPER + CTRL + Down` | Next empty workspace on this monitor |
| `SUPER + Scroll`, `SUPER + CTRL + Scroll` | Cycle workspaces on this monitor |
| `SUPER + S` | Toggle the special workspace |
| `SUPER + SHIFT + S` | Move window to the special workspace |

`NUM_WPM = 5` matches Orbit's five-workspace Home blocks per monitor.

## Hardware and gestures

Volume, microphone, media and brightness keys call `noctalia msg` (`volume-up`,
`mic-mute`, `media toggle`, `brightness-up`, …). Touchpad gestures follow the
CachyOS defaults: four-finger horizontal swipe switches workspaces; three-finger
down closes, up toggles fullscreen, left toggles floating.

## Changing binds

Everything lives in the "Keybindings" section of
[`config/hypr/hyprland.lua`](../config/hypr/hyprland.lua). Application choices
are the `TERMINAL`, `FILE_MANAGER`, `BROWSER`, `EDITOR`, `CALCULATOR`, and
`TASK_MANAGER` variables at the top of the file; set `launchPrefix` to
`"uwsm app -- "` if you start Hyprland through UWSM.
