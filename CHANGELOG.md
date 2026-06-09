# Changelog

All notable changes to FletX.

---

## [0.1.5] — 2026-06-09

### Flet 0.85+ Compatibility
- `flet>=0.85.0` requirement — full `ft.Router` integration with `manage_views=True` and native platform transitions.

### ft.Router Backend (`router_backend="flet"`)
- New `FletRouterBackend` — delegates rendering to `ft.Router` while `FletXRouter` keeps all logic (guards, middleware, history, resolvers).
- `FletXApp(router_backend="flet")` selects the backend; `"fletx"` (default) keeps existing behavior.
- `FletXRouter` API is **identical** in both modes — no code changes needed.

### Nested Routes with Outlet
```python
router_config.add_route("/settings", SettingsShell, outlet=True)
router_config.add_nested_routes("/settings", [
    {"path": "general",   "component": SettingsGeneral},
    {"path": "profile",   "component": SettingsProfile},
])

class SettingsShell(FletXPage):
    def build(self):
        return ft.Row([
            ft.NavigationRail(...),  # persistent shell
            self._outlet_content,    # active child
        ])
```
- `RouteDefinition.outlet` flag marks layout routes.
- `FletXPage._outlet_content` injected with rendered child BEFORE `build()`.
- Auto-generated index child for the parent URL default view.
- Deep nesting and `ModuleRouter` outlet support.

### Lifecycle-Aware Dialogs
- `FletXPage.show_dialog()`, `close_dialog()` — track state, auto-close on unmount.
- `alert(title, msg)`, `confirm(title, msg, on_confirm, on_cancel)` — one-liner helpers.
- `show_snack_bar(content)`, `hide_loader()` — convenience wrappers.

### Sync Navigation
- `FletXRouter.navigate_sync(route)` — safe from Flet event handlers (`on_click`, `on_change`).

### Flet CLI Passthrough
- `fletx build`, `debug`, `pack`, `publish`, `serve`, `emulators`, `devices`, `doctor` — full `--help` support.

### Fixed
- `ModuleRouter.__init__` crash when `sub_routers` not defined.
- `CommandParser` error on commands with only optional args (e.g. `doctor`).
- `add_nested_routes` path duplication in kwargs.
- `ModuleRouter._config` class var → instance var (stopped test pollution).
- History management: initial `/` no longer appended to stack.
- Test `sys.modules` pollution causing cascading ImportErrors (saved/restored in 3 test files).
- `build_navigation_widgets()` resilience (TypeError for Flet 0.85 `page.views` proxy).
- `page.push_route()` now properly awaited (async in Flet 0.85.3).
- `FletXRouter._instance` properly set in `router_backend="flet"` code path.

### Docs
- New `examples/outlet_demo/` — working nested route app.
- Comprehensive `api-reference.md`.
- Updated `routing.md`, `pages.md`, `architecture.md`, `fletx-cli.md`, `README.md`.

---

## [0.1.4] — 2025-12

- Initial Flet >=0.85.0 requirement (preparation).
- Dialog API on FletXPage.
- `ft.Router` experimental support.
- flet CLI passthrough commands.
- Cleaner comment style.

---

## [0.1.3] — 2025-10

- Flet 0.27-0.28 compatibility.
- Initial Obx widget support.

---

## [0.1.2] — 2025-08

- Flet 0.26-0.27 compatibility.
- Controller lifecycle improvements.

---

## [0.1.1] — 2025-07

- Flet 0.25-0.26 compatibility.
- Reactive state primitives (RxInt, RxList, Computed).

---

## [0.1.0] — 2025-06

- Initial release.
- `FletXApp`, `FletXPage`, `FletXController`, `RouterConfig`, `FletXRouter`.
- Decorators: `@obx`, `@register_router`, `@reactive_memo`, `@reactive_debounce`.
- CLI: `fletx new`, `generate`, `run`, `test`, `check`.
- Dependency injection via `FletX.find()` / `FletX.put()`.
- Route guards and middleware.
