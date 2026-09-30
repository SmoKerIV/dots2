#!/usr/bin/env python3
"""Deterministic contracts for the surviving Orbit/Hyprland architecture."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
BIN = REPO / "bin"
UNIT_DIR = REPO / "systemd/user"
HYPR = REPO / "config/hypr"
GLOBAL_MENU = REPO / "config/quickshell/global-menu"


def load(name: str, path: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CurrentArchitectureTests(unittest.TestCase):
    def test_current_files_and_syntax(self):
        required = (
            BIN / "orbit-app-launch",
            BIN / "orbit-appmenu",
            BIN / "orbit-appmenu-atspi",
            BIN / "orbit-input-state",
            BIN / "orbit-home-workspaces",
            BIN / "orbit-monitor",
            BIN / "orbit-session-transition",
            BIN / "orbit-home-workspaces",
            BIN / "orbit-theme",
            BIN / "orbit-wallpaper-control",
            BIN / "orbit-wallpaper-engine",
            BIN / "install-hyprglass",
            BIN / "install-scrolloverview",
            BIN / "workspace-alt-tab",
            BIN / "workspace-alt-tab-release",
            HYPR / "scripts/new-workspace-apps",
            HYPR / "scripts/window-shader-events",
            HYPR / "hyprland.lua",
            HYPR / "appearance.toml",
            GLOBAL_MENU / "shell.qml",
        )
        self.assertFalse([str(path) for path in required if not path.is_file()])

        shell_scripts = (
            BIN / "orbit-session-transition",
            BIN / "orbit-home-workspaces",
            BIN / "workspace-alt-tab-release",
            HYPR / "scripts/new-workspace-apps",
            HYPR / "scripts/window-shader-events",
        )
        for path in shell_scripts:
            self.assertTrue(os.access(path, os.X_OK), path)
            subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)
        for path in (BIN / "orbit-input-state", BIN / "orbit-monitor", BIN / "orbit-theme", BIN / "workspace-alt-tab"):
            compile(path.read_text(), str(path), "exec")

        for path in (REPO / "config").rglob("*.toml"):
            tomllib.loads(path.read_text())
        for path in (REPO / "config").rglob("*.json"):
            if path.name != "settings.json" or path.parent.name != "zed":
                json.loads(path.read_text())

    def test_current_startup_graph(self):
        hyprland = (HYPR / "hyprland.lua").read_text()
        self.assertIn('hl.exec_cmd("/usr/bin/noctalia &")', hyprland)
        self.assertIn(
            'quickshell .. " --config global-menu --no-duplicate &"',
            hyprland,
        )
        self.assertNotIn("orbit-shell", hyprland)
        self.assertNotIn("wallpaper-session-effects", hyprland)
        self.assertNotIn("quickshell/orbit", hyprland)

    def test_global_menu_config_is_current(self):
        source = "\n".join(path.read_text() for path in GLOBAL_MENU.glob("*.qml"))
        self.assertIn("ApplicationActionsSurface", source)
        self.assertIn("MenuSurface", source)
        self.assertIn("noctalia-global-menu-anchor", source)
        self.assertNotIn("quickshell/orbit", source)

    def test_removed_architecture_is_not_required(self):
        removed = (
            REPO / "config/quickshell/orbit",
            BIN / "orbit-shell",
            BIN / "orbit-shell-ui",
            REPO / "config/hyprshell",
            REPO / "config/hypr/scripts/hyprshell-start",
            UNIT_DIR / "orbit-shell.service",
            UNIT_DIR / "wallpaper-session-effects.service",
            REPO / "config/hypr/scripts/wallpaper-session-effects",
            BIN / "orbit-colors-extract.retired",
            BIN / "orbit-wallpaper-engine.pre-recovery-fix",
        )
        self.assertFalse([str(path) for path in removed if path.exists()])

    def test_current_units_and_session_target(self):
        target = (UNIT_DIR / "hyprland-session.target").read_text()
        for service in (
            "workspace-alt-tab-input.service",
            "workspace-alt-tab-release.service",
            "new-workspace-apps.service",
        ):
            self.assertIn(f"Wants={service}", target)

        expected_exec = {
            "orbit-wallpaper-engine.service": "%h/.local/bin/orbit-wallpaper-engine",
            "workspace-alt-tab-input.service": "/usr/bin/sg input -c %h/.local/bin/orbit-input-state",
            "workspace-alt-tab-release.service": "%h/.local/bin/workspace-alt-tab-release",
            "new-workspace-apps.service": "%h/.config/hypr/scripts/new-workspace-apps",
            "window-shader-events.service": "%h/.config/hypr/scripts/window-shader-events",
        }
        for unit, command in expected_exec.items():
            self.assertIn(f"ExecStart={command}", (UNIT_DIR / unit).read_text())

    def test_new_workspace_canonical_service_ownership_contract(self):
        service = (UNIT_DIR / "new-workspace-apps.service").read_text()
        script = (HYPR / "scripts/new-workspace-apps").read_text()
        self.assertIn("ExecStart=%h/.config/hypr/scripts/new-workspace-apps", service)
        self.assertIn("WantedBy=hyprland-session.target", service)
        self.assertIn("is_allowlisted", script)
        self.assertIn("openwindow>>", script)
        self.assertIn("flock -x 9", script)
        self.assertNotIn('hl.exec_cmd(scripts .. "/new-workspace-apps &")', (HYPR / "hyprland.lua").read_text())

    def test_plugins_are_configured_and_referenced(self):
        hyprland = (HYPR / "hyprland.lua").read_text()
        for name in (
            "hyprGlassPlugin",
            "hyprWindowShadePlugin",
            "scrollOverviewPlugin",
        ):
            self.assertIn(name, hyprland)

    def test_input_state_and_alt_tab_contract(self):
        unit = (UNIT_DIR / "workspace-alt-tab-input.service").read_text()
        helper = (BIN / "orbit-input-state").read_text()
        release = (BIN / "workspace-alt-tab-release").read_text()
        self.assertIn("orbit-input-state", unit)
        self.assertIn("RuntimeDirectory=orbit", unit)
        self.assertIn("pyudev", helper)
        self.assertIn("selectors", helper)
        self.assertIn("EAGAIN", helper)
        self.assertIn("ALT_CODES", helper)
        self.assertNotIn("ID_INPUT_KEYBOARD", helper)
        self.assertIn("alt-held", release)
        self.assertIn('workspace-alt-tab" close', release)

    def test_home_workspace_contract(self):
        helper = (BIN / "orbit-home-workspaces").read_text()
        alt_tab = (BIN / "workspace-alt-tab").read_text()
        self.assertIn("1 + index * 5", helper)
        self.assertIn("sort_by([(.x // 0), (.y // 0), (.name // \"\")])", helper)
        self.assertIn('rule.get("persistent") is True', alt_tab)
        self.assertIn('rule.get("default") is True', alt_tab)

    def test_input_module_contract(self):
        module = load("orbit_input_state_contract", BIN / "orbit-input-state")
        self.assertFalse(module.has_alt_capability({module.ecodes.EV_KEY: [30, 272]}))
        self.assertTrue(module.has_alt_capability({module.ecodes.EV_KEY: [56]}))
        self.assertTrue(module.has_alt_capability({module.ecodes.EV_KEY: [100]}))

    def test_wallpaper_and_transition_contract(self):
        wallpaper = (BIN / "orbit-wallpaper-engine").read_bytes()
        transition = (BIN / "orbit-session-transition").read_text()
        self.assertIn(b"ORBIT_WALLPAPER_CONTROL_FILE", wallpaper)
        self.assertIn("orbit-wallpaper-engine.service", transition)
        self.assertIn("orbit-session-transition", transition)
        self.assertNotIn(b"ps3-wave-wallpaper", wallpaper)
        self.assertNotIn("wallpaper-session-effects", transition)

    def test_wallpaper_external_integration_install_contract(self):
        installer = (BIN / "dotfiles-install-wallpaper").read_text()
        self.assertIn("integrations/noctalia", installer)
        self.assertIn("orbit-wallpaper-settings", installer)
        self.assertIn("orbit-wallpaper-engine-settings.desktop", installer)
        self.assertIn("install_noctalia_integration", installer)
        self.assertIn('ORBIT_WALLPAPER_REF:-v0.2.0', installer)

    def test_pinned_core_plugin_installers_contract(self):
        installers = {
            "install-hyprglass": (
                "https://github.com/hyprnux/hyprglass.git",
                "5bc835dcc909cef6980291688143048cf16942b5",
                "make",
                "hyprglass.so",
            ),
            "install-scrolloverview": (
                "https://github.com/yayuuu/hyprland-scroll-overview.git",
                "f9248ab6bee770e9d68813b48cc6ca12b3271254",
                "make all",
                "libscrolloverview.so",
            ),
        }
        tracked = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "*.so"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual(tracked, "")
        for name, (url, revision, build, output) in installers.items():
            path = BIN / name
            source = path.read_text()
            self.assertTrue(os.access(path, os.X_OK), path)
            self.assertIn(url, source)
            self.assertIn(revision, source)
            self.assertIn(build, source)
            self.assertIn(output, source)
            self.assertNotIn("origin/main", source)
            self.assertNotIn("refs/heads/main", source)
            self.assertIn("source_dir=", source)
            self.assertIn("plugin_dir=", source)
            self.assertNotIn('source_dir="$REPO', source)

    def test_wallpaper_launcher_routes_through_hyprland_placement(self):
        launcher = (BIN / "orbit-wallpaper-launcher").read_text()
        desktop = (REPO / "desktop/orbit-wallpaper-engine-settings.desktop").read_text()
        self.assertIn("hl.dsp.exec_cmd", launcher)
        self.assertIn('size = { 560, 760 }', launcher)
        self.assertIn('monitor_w-560-20', launcher)
        self.assertIn('45 }', launcher)
        self.assertIn("Exec=orbit-wallpaper-launcher", desktop)
        self.assertNotIn("Exec=orbit-wallpaper-settings", desktop)


class CachyOSPortTests(unittest.TestCase):
    """The CachyOS/Arch port: default binds preserved, no Fedora-only paths."""

    def test_hyprland_binds_follow_cachyos_defaults(self):
        hyprland = (HYPR / "hyprland.lua").read_text()
        for snippet in (
            'hl.bind(mainMod .. " + Return",     hl.dsp.exec_cmd(launchPrefix .. terminal))',
            'hl.bind(mainMod .. " + Q",           hl.dsp.window.close())',
            'hl.bind(mainMod .. " + Space",      hl.dsp.exec_cmd(launcher))',
            'hl.bind(mainMod .. " + E",          hl.dsp.exec_cmd(launchPrefix .. fileManager))',
            'hl.bind(mainMod .. " + W",          hl.dsp.exec_cmd(launchPrefix .. BROWSER))',
            'hl.bind(mainMod .. " + V", hl.dsp.exec_cmd(noctCall .. "panel-toggle clipboard"))',
            'hl.bind(mainMod .. " + S",         hl.dsp.workspace.toggle_special())',
            'hl.bind("Print",               hl.dsp.exec_cmd(noctCall .. "screenshot-region"))',
            'hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd(noctCall .. "volume-up")',
            'hl.bind(mainMod .. " + CONTROL + Down",  hl.dsp.focus({ workspace = "emptym" }))',
            'return "code:" .. (d == 0 and 19 or (9 + d))',
        ):
            self.assertIn(snippet, hyprland, snippet)
        # Same keys, Orbit implementation.
        self.assertIn('hl.bind("ALT + Tab",         hl.dsp.exec_cmd(workspaceAltTab .. " cycle"))', hyprland)
        self.assertIn('hl.bind(mainMod .. " + L",          hl.dsp.exec_cmd(animateLock))', hyprland)
        self.assertIn('hl.dsp.exec_cmd(focusDirectional .. " " .. direction)', hyprland)
        self.assertIn('hl.dsp.exec_cmd(moveWindowWorkspace .. " " .. direction)', hyprland)
        self.assertIn('TASK_MANAGER = "missioncenter"', hyprland)
        # Orbit-only extras live on keys the CachyOS layout leaves free.
        for snippet in (
            'hl.bind(mainMod .. " + ALT + A",   hl.dsp.exec_cmd(chatGPT))',
            'hl.bind(mainMod .. " + ALT + S",   hl.dsp.exec_cmd(openCode))',
            'hl.bind(mainMod .. " + ALT + D",   hl.dsp.exec_cmd(dailyNote))',
            'hl.bind(mainMod .. " + SHIFT + D", hl.dsp.exec_cmd(scratchpad))',
        ):
            self.assertIn(snippet, hyprland, snippet)
        # Old Orbit-only bindings that collide with CachyOS keys are gone.
        self.assertNotIn('hl.bind(mainMod .. " + C", hl.dsp.window.close())', hyprland)
        self.assertNotIn('hl.bind(mainMod .. " + A", hl.dsp.exec_cmd(chatGPT))', hyprland)
        self.assertNotIn("flatpak", hyprland)
        # Fresh installs have neither monitors.lua nor noctalia.lua yet.
        self.assertIn('if not pcall(require, "monitors") then', hyprland)
        self.assertIn('pcall(function() require("noctalia").apply_theme() end)', hyprland)
        subprocess.run(["luac", "-p", str(HYPR / "hyprland.lua")], check=True, capture_output=True)

    def test_units_use_arch_paths(self):
        polkit = (UNIT_DIR / "hyprpolkitagent.service").read_text()
        self.assertIn("ExecStart=/usr/lib/hyprpolkitagent/hyprpolkitagent", polkit)
        self.assertNotIn("libexec", polkit)
        localsend = (UNIT_DIR / "localsend.service").read_text()
        self.assertIn("ExecStart=%h/.local/bin/show-localsend --daemon", localsend)
        for unit in UNIT_DIR.rglob("*"):
            if unit.is_file():
                self.assertNotIn("flatpak", unit.read_text(), unit)
        self.assertTrue((UNIT_DIR / "sunshine.service.d/orbit-display.conf").is_file())
        self.assertIn("sunshine.service", (BIN / "orbit-sunshine-display").read_text())

    def test_noctalia_shell_config_owns_orbit_boundaries(self):
        config = tomllib.loads((REPO / "config/noctalia/50-orbit-shell.toml").read_text())
        self.assertFalse(config["shell"]["polkit_agent"])
        self.assertFalse(config["wallpaper"]["enabled"])
        self.assertFalse(config["lockscreen"]["enabled"])
        self.assertIn("Top", config["bar"])
        self.assertIn("hyprland", config["theme"]["templates"]["builtin_ids"])
        self.assertIn("wezterm", config["theme"]["templates"]["builtin_ids"])
        self.assertIn("orbit_wallpaper_palette", config["theme"]["templates"]["user"])

    def test_pinned_cachyos_installers(self):
        installers = {
            "install-dynamic-cursors": (
                "https://github.com/virtcode/hypr-dynamic-cursors.git",
                "5a224284872208b5324759d535d65061043725de",
                "out/dynamic-cursors.so",
            ),
            "install-oblique-cursor": (
                "https://github.com/kayxean/oblique-cursor.git",
                "ecddc552b8a5eb53fbf7498f0e60fbd634906b4a",
                "dist/theme_",
            ),
        }
        for name, (url, revision, artifact) in installers.items():
            path = BIN / name
            source = path.read_text()
            self.assertTrue(os.access(path, os.X_OK), path)
            self.assertIn(url, source)
            self.assertIn(revision, source)
            self.assertIn(artifact, source)
        shade = (BIN / "install-hyprwindowshade").read_text()
        self.assertIn("pkg-config --exists hyprland", shade)
        self.assertIn("/var/cache/hyprpm", shade)
        for name in ("install-gpu-screen-recorder", "install-actions-for-nautilus"):
            self.assertIn("pacman", (BIN / name).read_text(), name)
        self.assertNotIn("dnf", (BIN / "install-actions-for-nautilus").read_text())
        for path in BIN.iterdir():
            if path.is_file():
                self.assertNotIn(b"dnf install", path.read_bytes(), path)

    def test_bootstrap_scripts_for_cachyos(self):
        for name in ("takeover", "install-packages", "install-cachyos", "deploy", "verify"):
            path = REPO / "bootstrap" / name
            self.assertTrue(os.access(path, os.X_OK), path)
            subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)
        packages = (REPO / "bootstrap/install-packages").read_text()
        for package in ("hyprland", "hyprpm", "noctalia", "quickshell", "nwg-displays", "python-evdev", "ttf-jetbrains-mono", "hyprqt6engine"):
            self.assertIn(package, packages)
        with tempfile.TemporaryDirectory() as home:
            listing = subprocess.run(
                [str(REPO / "bootstrap/deploy"), "--list"],
                check=True, capture_output=True, text=True, env={**os.environ, "HOME": home},
            ).stdout
        self.assertIn(f"link\t{REPO}/config/noctalia/50-orbit-shell.toml\t{home}/.config/noctalia/50-orbit-shell.toml", listing)
        self.assertIn(f"seed\t{REPO}/config/hypr/monitors.example.lua\t{home}/.config/hypr/monitors.lua", listing)
        self.assertIn(f"link\t{REPO}/systemd/user/sunshine.service.d/orbit-display.conf", listing)

    def test_plymouth_theme_is_distro_neutral(self):
        script = (REPO / "plymouth/orbit/orbit.script").read_text()
        self.assertIn('Image("logo.png")', script)
        self.assertNotIn("fedora", script.lower())
        self.assertFalse((REPO / "plymouth/orbit/fedora-logo-icon.png").exists())
        installer = (BIN / "install-plymouth-theme").read_text()
        self.assertIn("plymouth-set-default-theme -R orbit", installer)
        self.assertIn("/usr/share/plymouth/themes/cachyos/watermark.png", installer)

    def test_greeter_sync_is_gated_on_greetd(self):
        sync = (BIN / "orbit-sync-noctalia-greeter").read_text()
        self.assertIn("systemctl is-enabled --quiet greetd.service", sync)


if __name__ == "__main__":
    unittest.main()
