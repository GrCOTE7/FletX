# API Reference

## FletXApp

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_route` | `str` | `"/"` | Initial route path |
| `navigation_mode` | `NavigationMode` | `VIEWS` | Router navigation mode |
| `router_backend` | `str` | `"fletx"` | `"fletx"` or `"flet"` (ft.Router, needs Flet >= 0.85.0) |
| `theme_mode` | `ThemeMode` | `SYSTEM` | Light / dark / system |
| `debug` | `bool` | `False` | Enable debug logging |
| `title` | `str` | `"FletX App"` | App window title |
| `theme` | `Theme` | `None` | Light theme |
| `dark_theme` | `Theme` | `None` | Dark theme |
| `window_config` | `dict` | `{}` | Window properties (width, height, etc.) |
| `on_startup` | `Callable | list` | `None` | Startup hook(s) |
| `on_shutdown` | `Callable | list` | `None` | Shutdown hook(s) |

**Methods:**

| Method | Description |
|--------|-------------|
| `run(**kwargs)` | Run app synchronously |
| `run_async(**kwargs)` | Run app asynchronously |
| `run_web(host, port, **kwargs)` | Run as web app |
| `run_desktop(**kwargs)` | Run as desktop app |
| `add_startup_hook(callable)` | Add startup hook |
| `add_shutdown_hook(callable)` | Add shutdown hook |
| `configure_window(**config)` | Set window properties |
| `configure_theme(theme, dark_theme)` | Set themes |

---

## FletXPage

Base class for all pages. Extends `ft.Container`.

**Lifecycle hooks:**

| Hook | When |
|------|------|
| `on_init()` | Page becomes active |
| `did_mount()` | Page attached to view |
| `will_unmount()` | Before removal |
| `did_unmount()` | After removal |
| `on_destroy()` | Page will unmount |

**Abstract:**

| Method | Returns | Description |
|--------|---------|-------------|
| `build()` | `Control | list[Control]` | Builds the page UI (required) |

**Navigation widgets (override to provide):**

| Method | Returns |
|--------|---------|
| `build_app_bar()` | `Optional[AppBar]` |
| `build_drawer()` | `Optional[NavigationDrawer]` |
| `build_end_drawer()` | `Optional[NavigationDrawer]` |
| `build_bottom_app_bar()` | `Optional[BottomAppBar]` |
| `build_navigation_bar()` | `Any` |
| `build_floating_action_button()` | `Optional[FloatingActionButton]` |
| `build_bottom_sheet()` | `BottomSheet` |

**Dialogs:**

| Method | Description |
|--------|-------------|
| `show_dialog(dialog)` | Show a custom AlertDialog (lifecycle-tracked) |
| `close_dialog()` | Close the tracked dialog |
| `alert(title, message)` | Simple alert with OK button |
| `confirm(title, message, on_confirm, on_cancel)` | Confirmation dialog |
| `show_loader(content)` | Show loading dialog (ProgressRing) |
| `hide_loader()` | Close loader dialog |
| `show_snack_bar(content, action, duration)` | Show SnackBar notification |

**Navigation helpers:**

| Method | Description |
|--------|-------------|
| `open_drawer()` / `close_drawer()` | Navigation drawer |
| `open_end_drawer()` / `close_end_drawer()` | End drawer |
| `open_bottom_sheet(content, on_dismiss)` | Bottom sheet |
| `set_app_bar(app_bar)` | Set app bar programmatically |
| `set_floating_action_button(fab, location)` | Set FAB |
| `set_drawer(drawer)` | Set drawer |
| `set_title(title)` | Set page title |
| `set_theme_mode(theme_mode)` | Set theme |

**Layout outlet:**

| Attribute | Description |
|-----------|-------------|
| `_outlet_content` | Injected child component (only when page is an `outlet=True` layout route) |

---

## RouterConfig

Global route configuration (`fletx.core.routing.config.router_config`).

**Methods:**

| Method | Description |
|--------|-------------|
| `add_route(path, component, *, outlet=False, guards, middleware, resolve, meta)` | Add single route |
| `add_routes(routes_list)` | Add multiple routes from dict list |
| `add_nested_routes(parent_path, routes_list)` | Add child routes under parent |
| `add_module_routes(base_path, module_router)` | Mount a ModuleRouter |
| `get_route(path)` | Get route definition by path |
| `match_route(path)` | Match path against patterns |
| `get_all_routes()` | Get all registered routes |

**Route dict keys:**

```python
{"path": str, "component": Type[FletXPage] | Callable,
 "outlet": bool,     # layout route (ft.Router backend)
 "guards": list,     # RouteGuard instances
 "middleware": list, # RouteMiddleware instances
 "resolve": dict,    # key → data resolver callable
 "meta": dict}       # arbitrary metadata
```

---

## FletXRouter

Singleton router (`FletXRouter.get_instance()`).

**Methods:**

| Method | Description |
|--------|-------------|
| `navigate(route, *, data, replace, clear_history)` | Async navigate |
| `navigate_sync(route, **kwargs)` | Sync-safe navigate for event handlers |
| `navigate_with_intent(intent)` | Navigate with NavigationIntent |
| `go_back()` | Navigate back |
| `go_forward()` | Navigate forward |
| `can_go_back()` | Check if can go back |
| `can_go_forward()` | Check if can go forward |
| `get_current_route()` | Get current RouteInfo |
| `get_history()` | Get navigation history |
| `add_global_guard(guard)` | Add global route guard |
| `add_global_middleware(middleware)` | Add global middleware |
| `set_navigation_mode(mode)` | Set NavigationMode |

---

## RouteDefinition

Dataclass representing one route:

| Field | Type | Description |
|-------|------|-------------|
| `path` | `str` | Route path (e.g. `"/user/:id"`) |
| `component` | `Type | Callable` | Page class or callable |
| `outlet` | `bool` | Layout route (ft.Router backend) |
| `route_type` | `RouteType` | PAGE, VIEW, NESTED, REDIRECT, MODULE |
| `guards` | `list[RouteGuard]` | Route-level guards |
| `middleware` | `list[RouteMiddleware]` | Route-level middleware |
| `resolve` | `dict[str, Callable]` | Data resolvers |
| `children` | `list[RouteDefinition]` | Child routes |
| `parent` | `RouteDefinition` | Parent route |
| `meta` | `dict` | Arbitrary metadata |

---

## ModuleRouter

Sub-router for feature-based route organization:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Module name |
| `base_path` | `str` | URL prefix |
| `routes` | `list[dict]` | Route definitions |
| `sub_routers` | `list[Type[ModuleRouter]]` | Nested sub-routers |
| `is_root` | `bool` | Mark as root router |

```python
@register_router
class AdminRouter(ModuleRouter):
    name = "admin"
    base_path = "/admin"
    is_root = False
    routes = [
        {"path": "/", "component": AdminShell, "outlet": True},
        {"path": "/users", "component": UsersPage},
    ]
```

---

## Guards & Middleware

### RouteGuard

| Method | Description |
|--------|-------------|
| `can_activate(route_info)` | Check if route can be entered |
| `can_deactivate(route_info)` | Check if route can be left |
| `redirect_to(route_info)` | Where to redirect if blocked |

### RouteMiddleware

| Method | Description |
|--------|-------------|
| `before_navigation(from_route, to_route)` | Called before navigating |
| `after_navigation(route_info)` | Called after successful navigation |
| `on_navigation_error(error, route_info)` | Called on navigation error |
