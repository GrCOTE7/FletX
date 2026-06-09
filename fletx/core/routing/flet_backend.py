"""
Flet Router Backend for FletX

Integrates FletX's routing logic with Flet's native ``ft.Router``
(available since Flet 0.85.0). The backend handles view management
and rendering via ``page.render_views()``, while ``FletXRouter``
owns the logic layer: guards, middleware, history, and data resolution.

Architecture
------------
FletXRouter (logic)
    │  navigate() runs guards → middleware → resolvers → history
    │  creates FletXPage instance, builds it
    │
    └── FletRouterBackend (rendering)
         │  receives pre-built FletXPage → wraps in ft.View → page.push_route()
         │  ft.Router matches URL → wrapper @ft.component constructs View
         │  lifecycle (did_mount/will_unmount) via use_effect hooks
         │  system back / view pop handled natively by ft.Router with state sync

Requires **flet >= 0.85.0**.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import flet as ft

from fletx.core.routing.config import RouterConfig
from fletx.core.routing.models import RouteInfo
from fletx.core.page import FletXPage

_logger = logging.getLogger("FletX.FletBackend")


class FletRouterBackend:
    """
    View-rendering backend powered by ``ft.Router``.

    Mounts a declarative ``ft.Router`` that manages ``page.views``
    via ``page.render_views()`` with ``manage_views=True``. Each route
    returns an ``ft.View`` wrapping the corresponding ``FletXPage``.

    Parameters
    ----------
    page : ft.Page
        The Flet page to mount the router onto.
    config : RouterConfig
        FletX route configuration (flattened, including ModuleRouter routes).
    initial_route : str
        Initial route to render after mounting (default ``"/"``).
    fletx_router :
        Reference to the ``FletXRouter`` instance for state synchronisation
        on external route changes (e.g. system back button).
    """

    def __init__(
        self,
        page: ft.Page,
        config: RouterConfig,
        initial_route: str = "/",
        fletx_router=None,
    ):
        self.page = page
        self._config = config
        self._initial_route = initial_route
        self._fletx_router = fletx_router

        self._ready = False

        # Flag set to True during FletXRouter-initiated navigations
        # so _sync_external_route() skips state sync (which was
        # already handled by FletXRouter before calling navigate()).
        self._navigating = False

        # route path → (FletXPage instance, RouteInfo)
        # Populated by navigate() before push_route(), consumed by
        # the wrapper @ft.component during its build cycle.
        self._pending_instances: Dict[str, tuple] = {}

        # route path → FletXPage (currently active)
        # Maintained for debugging and future rehydration support.
        self._active_instances: Dict[str, FletXPage] = {}

    # ── public API ───────────────────────────────────────────────────

    @staticmethod
    def check_version() -> bool:
        """
        Verify that ``ft.Router`` is available in the installed Flet version.

        Returns ``True`` if the backend can be used, ``False`` otherwise.
        """
        try:
            import flet as _ft
            return hasattr(_ft, "Router") and hasattr(_ft, "Route")
        except Exception:
            return False

    def mount(self):
        """
        Explicitly build and mount the ``ft.Router`` onto the page.

        Should be called once during app initialisation, after the
        page is ready but before the first navigation.
        """
        self._ensure_router()

    async def navigate(
        self,
        route: str,
        instance: FletXPage,
        route_info: RouteInfo,
        *,
        replace: bool = False,
    ):
        """
        Push a pre-built ``FletXPage`` for rendering via ``ft.Router``.

        The *instance* must already have ``_build_page()`` called.
        The backend stores it in a pending registry, then triggers
        a route change so ``ft.Router`` re-renders and the wrapper
        ``@ft.component`` picks up the instance.

        Parameters
        ----------
        route : str
            Target route path (e.g. ``"/user/42"``).
        instance : FletXPage
            Pre-built page component.
        route_info : RouteInfo
            Route metadata (params, data, query, etc.).
        replace : bool
            If ``True``, replace the current route instead of pushing.
        """
        self._ensure_router()
        self._pending_instances[route] = (instance, route_info)

        # The page.push_route / page.navigate calls below trigger
        # page.on_route_change synchronously.  Set the navigating
        # flag so our wrapped handler skips state sync.
        self._navigating = True
        try:
            if replace:
                self.page.navigate(route)
            else:
                await self.page.push_route(route)
        finally:
            self._navigating = False

    def go_back(self, previous_url: str):
        """
        Navigate back one step.

        Calls ``page.navigate(previous_url)``; ``ft.Router`` re-renders
        and the wrapper constructs the matching ``FletXPage``.
        """
        self._ensure_router()
        self._navigating = True
        try:
            self.page.navigate(previous_url)
        finally:
            self._navigating = False

    def close(self):
        """Release all tracked references."""
        self._pending_instances.clear()
        self._active_instances.clear()

    # ── internal setup ───────────────────────────────────────────────

    def _ensure_router(self):
        """Lazily build and mount the ``ft.Router``."""
        if self._ready:
            return

        all_routes = self._config.get_all_routes()
        flet_routes = self._build_flet_routes(all_routes)

        @ft.component
        def _router_component():
            return ft.Router(routes=flet_routes, manage_views=True)

        self.page.render_views(_router_component)

        # Hook into route changes that originate outside FletXRouter
        # (e.g. system back button, browser history).  ft.Router already
        # overwrites ``page.on_route_change`` inside its ``use_effect``,
        # so we wrap it *after* ``render_views()`` returns.
        original_handler = self.page.on_route_change
        backend_ref = self

        def _wrapped_on_route_change(e: ft.RouteChangeEvent):
            backend_ref._sync_external_route(e.route)
            if original_handler is not None:
                original_handler(e)

        self.page.on_route_change = _wrapped_on_route_change

        self._ready = True
        _logger.info(
            "Flet Router backend mounted (%d routes)", len(flet_routes)
        )

    def _build_flet_routes(self, routes_dict: Dict[str, Any]) -> list:
        """
        Convert the flat ``RouterConfig`` routes into a nested
        ``ft.Route`` tree.

        Routes with ``outlet=True`` and ``children`` become layout
        routes.  Each such parent gets an auto-generated ``index=True``
        child (using the first real child's component) so navigating to
        the parent URL shows a default view inside the outlet.

        Routes without ``outlet=True`` that have children are treated
        as flat, independent entries (backward-compatible with the
        traditional FletX flat routing model).
        """
        # Partition routes
        root_routes: Dict[str, Any] = {}     # path → RouteDefinition (no parent)
        child_map: Dict[str, list] = {}      # parent_path → [RouteDefinition]

        for path, route_def in routes_dict.items():
            if route_def.parent is not None:
                child_map.setdefault(route_def.parent.path, []).append(route_def)
            else:
                root_routes[path] = route_def

        # Also ensure children declared via RouteDefinition.children are
        # present in child_map (ModuleRouter routes added via
        # add_module_routes may set children but not parent references).
        for path, route_def in routes_dict.items():
            for child_def in route_def.children:
                child_map.setdefault(path, []).append(child_def)

        processed = set()
        flet_routes = []

        for path, route_def in root_routes.items():
            ft_route = self._convert_route(
                full_path=path,
                flet_path=path.lstrip("/") if path != "/" else "",
                route_def=route_def,
                child_map=child_map,
                processed=processed,
            )
            if ft_route is not None:
                flet_routes.append(ft_route)

        # Any remaining routes that were children of non-outlet parents
        # (or ModuleRouter routes without parent references) — add as
        # flat, standalone top-level entries.
        for path, route_def in routes_dict.items():
            if path in processed:
                continue
            if route_def.component is None:
                continue
            if path == "/":
                ft_route = ft.Route(
                    index=True,
                    component=self._make_wrapper(path, route_def.component),
                )
            else:
                ft_route = ft.Route(
                    path=path.lstrip("/"),
                    component=self._make_wrapper(path, route_def.component),
                )
            flet_routes.append(ft_route)
            processed.add(path)

        return flet_routes

    def _convert_route(
        self,
        full_path: str,
        flet_path: str,
        route_def,
        child_map: Dict[str, list],
        processed: set,
    ):
        """
        Recursively convert a ``RouteDefinition`` into an ``ft.Route``.

        ``full_path`` is the absolute FletX route (e.g. ``"/settings"``).
        ``flet_path`` is the path segment relative to the parent in the
        ``ft.Route`` tree (e.g. ``"settings"``).

        Outlet parents produce a tree with children; leaf routes produce
        a simple ``ft.Route``.
        """
        if full_path in processed:
            return None
        processed.add(full_path)

        children = child_map.get(full_path, [])

        if children and route_def.outlet:
            # Outlet layout route — children render inside the outlet
            child_routes = []
            index_component = None
            first_child_component = None

            for child_def in children:
                # Compute the path segment relative to this parent
                child_flet_path = _relative_flet_path(
                    child_def.path, full_path
                )
                child_ft = self._convert_route(
                    full_path=child_def.path,
                    flet_path=child_flet_path,
                    route_def=child_def,
                    child_map=child_map,
                    processed=processed,
                )
                if child_ft is not None:
                    child_routes.append(child_ft)
                    if first_child_component is None:
                        first_child_component = child_def.component
                    # Use the first non-outlet child's component for the
                    # auto-generated index route (the default view when
                    # navigating to the parent URL with no further path).
                    if index_component is None and not child_def.outlet:
                        index_component = child_def.component

            # Auto-generate an index child so navigating to the parent
            # URL shows a default view inside the outlet.  Falls back
            # to the first child's component if all children are outlets.
            if index_component is None and first_child_component is not None:
                index_component = first_child_component  # pragma: no cover

            if index_component is not None:
                child_routes.insert(
                    0,
                    ft.Route(
                        index=True,
                        component=self._make_wrapper(
                            full_path, index_component,
                        ),
                    ),
                )

            parent_seg = None if full_path == "/" else flet_path
            return ft.Route(
                path=parent_seg,
                outlet=True,
                component=self._make_wrapper(
                    full_path, route_def.component, outlet_parent=True,
                ),
                children=child_routes,
            )
        else:
            # Leaf route (or parent without outlet)
            if full_path == "/":
                return ft.Route(
                    index=True,
                    component=self._make_wrapper(full_path, route_def.component),
                )
            seg = None if full_path == "/" else flet_path
            return ft.Route(
                path=seg,
                component=self._make_wrapper(full_path, route_def.component),
            )

    def _sync_external_route(self, new_route: str):
        """
        Synchronise ``FletXRouter`` state when the route changes
        from outside (system back, browser back).
        """
        router = self._fletx_router
        if router is None:
            return

        # Skip when we initiated the navigation ourselves.
        if self._navigating:
            return

        current_path = router.state.current_route.path
        if new_route == current_path:
            return

        # Pop from history if the new route is the previous one
        if router.state.history and router.state.history[-1].path == new_route:
            prev_route = router.state.history.pop()
            router.state.forward_stack.append(router.state.current_route)
            router.state.current_route = prev_route
            _logger.debug("State synced: back → %s", new_route)

    # ── component wrapper ────────────────────────────────────────────

    def _make_wrapper(
        self, route_key: str, component_cls, *, outlet_parent: bool = False,
    ):
        """
        Create an ``@ft.component`` wrapper for a route.

        When ``ft.Router`` activates this route, the wrapper:
        1. Looks for a pre-created instance in ``_pending_instances``
           (put there by ``navigate()``).
        2. Falls back to creating a fresh instance (for back navigation
           where the component was not pre-built by FletXRouter).
        3. For *outlet_parent* routes, calls ``use_route_outlet()`` and
           injects the child content as ``_outlet_content`` so the page
           can include it in ``build()``.
        4. Wraps the instance in an ``ft.View`` and builds navigation
           widgets.
        5. Hooks ``did_mount`` / ``will_unmount`` lifecycle via
           ``use_effect``.
        """

        @ft.component
        def _wrapper(key=route_key, cls=component_cls, backend=self):
            # Resolve child content for outlet parent routes
            outlet_content = None
            if outlet_parent:
                outlet_content = ft.use_route_outlet()

            # Pre-created instance from FletXRouter.navigate()
            pending = backend._pending_instances.pop(key, None)

            if pending is not None:
                instance, route_info = pending
                instance.route_info = route_info
            else:
                # Back navigation or initial mount — create fresh
                instance = cls()
                instance.route_info = RouteInfo(path=key)

            # Inject outlet content BEFORE _build_page() so the page's
            # build() method can access it via self._outlet_content.
            if outlet_content is not None:
                instance._outlet_content = outlet_content

            # Build page content.  _build_page() internally calls
            # build_navigation_widgets() which is now safe to run
            # (it returns early when the View is not yet in page.views).
            # Navigation widgets are then applied on the View below.
            if hasattr(instance, "_build_page"):
                instance._build_page()

            # Wrap in ft.View for manage_views=True
            view = ft.View(route=key, controls=[instance])

            # Build navigation widgets onto the View
            _apply_nav_widgets(view, instance)

            # Lifecycle via Flet hooks
            ft.use_effect(
                setup=lambda: instance.did_mount(),
                dependencies=[],
                cleanup=lambda: instance.will_unmount(),
            )

            backend._active_instances[key] = instance
            return view

        return _wrapper


# ── helpers ────────────────────────────────────────────────────────


def _relative_flet_path(child_full: str, parent_full: str) -> str:
    """Compute the relative ``ft.Route`` path segment for a child route."""
    if parent_full == "/":
        return child_full.lstrip("/")
    return child_full[len(parent_full):].lstrip("/")


def _apply_nav_widgets(view: ft.View, instance: FletXPage):
    """Copy navigation widgets from a ``FletXPage`` onto a ``ft.View``."""

    appbar = instance.build_app_bar()
    if appbar is not None:
        view.appbar = appbar

    drawer = instance.build_drawer()
    if drawer is not None:
        view.drawer = drawer

    end_drawer = instance.build_end_drawer()
    if end_drawer is not None:
        view.end_drawer = end_drawer

    bottom = instance.build_bottom_app_bar()
    if bottom is not None:
        view.bottom_appbar = bottom

    nav_bar = instance.build_navigation_bar()
    if nav_bar is not None:
        view.navigation_bar = nav_bar

    fab = instance.build_floating_action_button()
    if fab is not None:
        view.floating_action_button = fab

    fab_loc = instance.build_floating_action_button_location()
    if fab_loc is not None:
        view.floating_action_button_location = fab_loc
