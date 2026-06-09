# Routing

> **TL;DR**: If you're coming from Flet, think of FletX routing like Angular/Vue Router for pages. Instead of manually managing `page.route` and `page.go()`, you declaratively define routes and let FletX handle the page lifecycle.

## What is Routing?

Routing in FletX manages navigation between different pages in your application. Instead of manually showing and hiding controls, you define routes that map URL paths to page components. When a user navigates to a path, FletX automatically displays the corresponding page.

### Why FletX Has Its Own Routing

Flet provides basic navigation through `page.route` and `page.go()`, but this approach requires manual page management. FletX builds on top of Flet's navigation to provide:

- **Declarative route definitions**: Define all routes in one place
- **Automatic page lifecycle**: Components are created and destroyed automatically
- **Data passing**: Send data between pages without global variables
- **Route parameters**: Handle dynamic paths like `/user/123`
- **Protection**: Guard sensitive routes with authentication checks
- **History management**: Built-in back/forward navigation

### Router Backend (Flet >= 0.85.0)

FletX offers two rendering backends. Choose at app init:

```python
from fletx.app import FletXApp

# FletX native backend (default, works with all Flet versions)
app = FletXApp(router_backend="fletx")

# Flet ft.Router backend (requires flet >= 0.85.0)
# Enables nested layouts with outlet, native platform transitions
app = FletXApp(router_backend="flet")
```

The **ft.Router backend** (`router_backend="flet"`) delegates view management to Flet's native `ft.Router` with `manage_views=True`. This gives you:

- Native platform transitions (iOS swipe-back, Android back gesture)
- Genuine nested route layouts with **outlet** support (parent shell persists while children swap)
- Automatic `page.views` stack management

The **FletX native backend** (`router_backend="fletx"`, default) handles everything directly via `page.controls` and `page.views`. All your existing code works unchanged.

**Note**: The `FletXRouter` API is identical regardless of backend. You never interact with the backend directly — `navigate()`, `go_back()`, `get_instance()`, guards, middleware, and all other APIs work the same way.

---

## Your First Route

Let's create a simple app with one route. First, define a page component:

```python
import flet as ft
from fletx.core import FletXPage

class HomePage(FletXPage):
    def build(self):
        return ft.Text("Welcome to the home page")
```

Now create your main app and register the route:

```python
from fletx import FletXApp
from fletx.navigation import router_config

# Register the route
router_config.add_routes([
    {"path": "/", "component": HomePage}
])

# Run the app
app = FletXApp()
app.run()
```

When the app starts, FletX navigates to `/` and displays your `HomePage` component.

**How it works:**
- `path`: The URL path to match (e.g., `/`, `/about`, `/settings`)
- `component`: The page class to display when the path matches
- FletX calls `build()` on your component to render the page

---

## Multiple Routes and Navigation

Let's add a second page and navigate between them:

```python
from fletx.core import FletXPage
from fletx.navigation import navigate
import flet as ft

class HomePage(FletXPage):
    def build(self):
        return ft.Column([
            ft.Text("Home Page"),
            ft.ElevatedButton(
                "Go to Settings",
                on_click=lambda _: navigate("/settings")
            )
        ])

class SettingsPage(FletXPage):
    def build(self):
        return ft.Column([
            ft.Text("Settings Page"),
            ft.ElevatedButton(
                "Go Back",
                on_click=lambda _: navigate("/")
            )
        ])
```

Register both routes:

```python
from fletx.navigation import router_config

router_config.add_routes([
    {"path": "/", "component": HomePage},
    {"path": "/settings", "component": SettingsPage}
])
```

### Going Back

Instead of navigating to a specific path, you can go back to the previous page:

```python
from fletx.navigation import go_back

ft.ElevatedButton("Back", on_click=lambda _: go_back())
```

This works like the browser's back button, returning to the last visited page.

---

## Passing Data Between Routes

Often you need to send data from one page to another. For example, clicking an item in a list to see its details.

**Sending page:**

```python
class ProductListPage(FletXPage):
    def build(self):
        def view_product(product_id, product_name):
            navigate("/product-details", data={
                "id": product_id,
                "name": product_name
            })
        
        return ft.Column([
            ft.ElevatedButton(
                "View Product A",
                on_click=lambda _: view_product(101, "Widget A")
            ),
            ft.ElevatedButton(
                "View Product B",
                on_click=lambda _: view_product(102, "Widget B")
            )
        ])
```

**Receiving page:**

```python
class ProductDetailsPage(FletXPage):
    def build(self):
        # Access the data passed from the previous page
        product_data = self.route_info.data
        product_id = product_data.get("id")
        product_name = product_data.get("name")
        
        return ft.Column([
            ft.Text(f"Product: {product_name}"),
            ft.Text(f"ID: {product_id}")
        ])
```

Register the route:

```python
router_config.add_routes([
    {"path": "/products", "component": ProductListPage},
    {"path": "/product-details", "component": ProductDetailsPage}
])
```

**When to use data passing:**
- Temporary data for a single navigation (like form data or selected item details)
- Data that doesn't need to persist across multiple page changes

---

## Dynamic Routes with Parameters

For URLs like `/user/123` or `/post/my-article`, use route parameters:

```python
router_config.add_routes([
    {"path": "/user/:user_id", "component": UserProfilePage}
])
```

The `:user_id` part matches any value in that position. Access it in your page:

```python
class UserProfilePage(FletXPage):
    def build(self):
        # Get the user_id from the URL
        user_id = self.route_info.params.get("user_id")
        
        return ft.Column([
            ft.Text(f"Viewing profile for user: {user_id}"),
            # Load user data based on user_id...
        ])
```

Navigate to these routes normally:

```python
# This will match /user/:user_id and set user_id to "123"
navigate("/user/123")

# This will match /user/:user_id and set user_id to "alice"
navigate("/user/alice")
```

**Multiple parameters:**

```python
router_config.add_routes([
    {"path": "/blog/:category/:post_id", "component": BlogPostPage}
])

# Access both parameters
class BlogPostPage(FletXPage):
    def build(self):
        category = self.route_info.params.get("category")
        post_id = self.route_info.params.get("post_id")
        
        return ft.Text(f"Category: {category}, Post: {post_id}")
```

---

## Nested Routes with Outlet

When building apps with shared layouts (admin panel with sidebar, settings with tabs), **outlet routes** let the parent shell persist while children swap inside it.

This feature requires the **ft.Router backend** (`router_backend="flet"`) and Flet >= 0.85.0.

### Mark a route as a layout

Use `outlet=True` on the parent route:

```python
from fletx.core.routing.config import router_config

# The layout that persists
router_config.add_route("/settings", SettingsShell, outlet=True)

# Children that render inside the layout's outlet
router_config.add_nested_routes("/settings", [
    {"path": "general",       "component": SettingsGeneral},
    {"path": "profile",       "component": SettingsProfile},
    {"path": "notifications", "component": SettingsNotifications},
])
```

### The layout page

The shell page uses `self._outlet_content` to render the active child:

```python
import flet as ft
from fletx.core import FletXPage
from fletx.core.routing.router import FletXRouter

class SettingsShell(FletXPage):
    def build(self):
        return ft.Row([
            # Left: persistent navigation
            ft.NavigationRail(
                destinations=[
                    ft.NavigationRailDestination(label="General"),
                    ft.NavigationRailDestination(label="Profile"),
                    ft.NavigationRailDestination(label="Notifications"),
                ],
                on_change=self._on_nav_change,
            ),
            ft.VerticalDivider(),
            # Right: child content renders here
            ft.Container(
                content=(
                    self._outlet_content
                    if self._outlet_content is not None
                    else ft.Text("Select a section")
                ),
                expand=True,
                padding=20,
            ),
        ], expand=True)

    def _on_nav_change(self, e):
        routes = {0: "/settings/general", 1: "/settings/profile",
                  2: "/settings/notifications"}
        FletXRouter.get_instance().navigate_sync(
            routes.get(e.control.selected_index, "/settings/general")
        )

    def build_app_bar(self):
        return ft.AppBar(title=ft.Text("Settings"))
```

### Child pages

Child pages are regular `FletXPage` subclasses — no special API needed:

```python
class SettingsGeneral(FletXPage):
    def build(self):
        return ft.Column([
            ft.Text("General Settings", size=22),
            ft.Switch(label="Dark mode", value=False),
            ft.TextField(label="App title", value="My App"),
        ])

class SettingsProfile(FletXPage):
    def build(self):
        return ft.Column([
            ft.Text("Profile Settings", size=22),
            ft.TextField(label="Display name", value="John"),
        ])
```

### How it works

When you navigate to `/settings/profile`:

1. The `SettingsShell` wrapper calls `ft.use_route_outlet()`, which renders the matched child (`SettingsProfile`)
2. The child content is injected as `self._outlet_content` BEFORE `build()` runs
3. `build()` returns the shell with the child content in the right panel
4. Navigating to `/settings/general` re-renders ONLY the child (shell persists)

An **auto-generated index child** uses the first non-outlet child's component, so navigating to `/settings` directly shows the general settings by default.

### Deep nesting

Outlet routes can be nested arbitrarily deep:

```python
# /admin → AdminShell
router_config.add_route("/admin", AdminShell, outlet=True)
router_config.add_nested_routes("/admin", [
    {"path": "settings", "component": SettingsShell, "outlet": True},
    {"path": "dashboard", "component": DashboardPage},
])
# /admin/settings → SettingsShell (nested outlet)
router_config.add_nested_routes("/admin/settings", [
    {"path": "general", "component": SettingsGeneral},
    {"path": "profile", "component": SettingsProfile},
])
```

### ModuleRouter with outlets

You can declare `outlet=True` in ModuleRouter route dicts:

```python
@register_router
class AdminRouter(ModuleRouter):
    name = "admin"
    base_path = "/admin"
    is_root = False
    routes = [
        {"path": "/", "component": AdminShell, "outlet": True},
        {"path": "/dashboard", "component": DashboardPage},
        {"path": "/users", "component": UsersPage},
    ]
```

### Synchronous navigation

`FletXRouter.navigate_sync(route)` is safe to call from Flet event handlers (`on_click`, `on_change`):

```python
from fletx.core.routing.router import FletXRouter

# From any FletXPage:
FletXRouter.get_instance().navigate_sync("/settings/profile")
```

It schedules the async `navigate()` on the event loop, so you never need to manage `await` in synchronous callbacks.

---

## Protected Routes with Guards

Route guards check conditions before allowing navigation. This is useful for authentication:

```python
from fletx.navigation import RouteGuard

class AuthGuard(RouteGuard):
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    async def can_activate(self, route_info):
        # Return True to allow, False to block
        return self.auth_service.is_logged_in()
    
    async def can_deactivate(self, route_info):
        # Optional: always allow leaving this route
        return True
    
    async def redirect_to(self, route_info):
        # Where to redirect if blocked
        return "/login"
```

Apply the guard to routes:

```python
# Assume you have an auth_service instance
auth_service = AuthService()

router_config.add_routes([
    {"path": "/login", "component": LoginPage},
    {
        "path": "/dashboard",
        "component": DashboardPage,
        "guards": [AuthGuard(auth_service)]  # Protected route
    }
])
```

Now if a user tries to access `/dashboard` without being logged in, they'll be redirected to `/login`.

---

## State and Controllers

When you navigate between pages, FletX destroys the previous page component and creates a new one. This means page-level state is lost.

To preserve state across navigation:

**Use Controllers (Services)**

Controllers exist outside the page lifecycle and maintain state:

```python
# cart_service.py
class CartService:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def get_items(self):
        return self.items
```

Use the same controller instance across pages:

```python
# In your app setup
cart_service = CartService()

class ProductPage(FletXPage):
    def build(self):
        def add_to_cart():
            cart_service.add_item({"name": "Widget", "price": 10})
        
        return ft.ElevatedButton("Add to Cart", on_click=lambda _: add_to_cart())

class CartPage(FletXPage):
    def build(self):
        items = cart_service.get_items()
        return ft.Column([
            ft.Text(f"Cart has {len(items)} items")
        ])
```

Even though you navigate between pages, the `cart_service` maintains its state.

---

## Advanced Features

### Modular Routing

For large applications, organize routes by feature using `ModuleRouter`:

```python
from fletx.navigation import ModuleRouter

# Create a module for admin routes
admin_module = ModuleRouter()
admin_module.add_routes([
    {"path": "/", "component": AdminHomePage},
    {"path": "/users", "component": AdminUsersPage}
])

# Mount the module under /admin
router_config.add_module_routes("/admin", admin_module)
```

This creates routes at `/admin/` and `/admin/users`.

**Decorator-based registration** (similar to Angular):

```python
from fletx.decorators import register_router

@register_router
class AdminRouter(ModuleRouter):
    name = 'Admin'
    base_path = '/admin'
    is_root = False
    routes = [
        {"path": "/", "component": AdminHomePage},
        {"path": "/users", "component": AdminUsersPage}
    ]
    sub_routers = []
```

### Page Transitions

Add animations when navigating between pages:

```python
from fletx.navigation import RouteTransition, TransitionType

router_config.add_routes([
    {
        "path": "/login",
        "component": LoginPage,
        "meta": {
            "transition": RouteTransition(
                transition_type=TransitionType.ZOOM_IN,
                duration=350
            )
        }
    }
])
```

### Middleware

Run code before and after navigation:

```python
from fletx.navigation import RouteMiddleware

class LoggingMiddleware(RouteMiddleware):
    def before_navigation(self, from_route, to_route):
        print(f"Navigating from {from_route.path} to {to_route.path}")
    
    def after_navigation(self, route_info):
        print(f"Arrived at {route_info.path}")

router_config.add_route(
    path="/analytics",
    component=AnalyticsPage,
    middleware=[LoggingMiddleware()]
)
```

---

## Best Practices

### Organize Routes in Files

For maintainability, define routes in a separate file:

```python
# routes.py
from fletx.navigation import router_config
from pages import HomePage, SettingsPage, ProfilePage

def setup_routes():
    router_config.add_routes([
        {"path": "/", "component": HomePage},
        {"path": "/settings", "component": SettingsPage},
        {"path": "/profile/:user_id", "component": ProfilePage}
    ])

# main.py
from fletx import FletXApp
from routes import setup_routes

setup_routes()
app = FletXApp()
app.run()
```

### Use Constants for Paths

Avoid hardcoding paths throughout your app:

```python
# constants.py
class Routes:
    HOME = "/"
    SETTINGS = "/settings"
    PROFILE = "/profile"

# Usage
navigate(Routes.SETTINGS)
```

### Data Passing Guidelines

- **Route data**: Use for temporary data in a single navigation flow
- **Controllers/Services**: Use for app-wide state that persists across navigation
- **Route parameters**: Use for identifiers that should appear in the URL

### Keep Pages Focused

Pages should handle UI rendering. Move business logic to controllers:

```python
# Good
class ProductPage(FletXPage):
    def build(self):
        products = product_service.get_all()  # Service handles logic
        return ft.Column([...])

# Avoid
class ProductPage(FletXPage):
    def build(self):
        # Don't put database queries and business logic here
        connection = connect_to_db()
        products = connection.query("SELECT * FROM products")
        ...
```

---

## Summary

| Feature | Purpose |
|---------|---------|
| `router_config.add_routes()` | Define path-to-component mappings |
| `navigate(path)` | Navigate to a route programmatically |
| `go_back()` | Return to the previous page |
| `navigate(path, data={...})` | Pass data to the next page |
| Route parameters (`:param`) | Handle dynamic URL segments |
| `RouteGuard` | Protect routes with conditions |
| `ModuleRouter` | Organize routes by feature |
| `RouteTransition` | Add page animations |
| `RouteMiddleware` | Hook into navigation lifecycle |

---

## Next Steps

- Learn about [Controllers](controllers.md) for managing application state
- Explore [Dependency Injection](dependency-injection.md) for providing services to pages
- Understand [Services](services.md) for shared business logic