"""
Flet Router Backend for FletX

Adapter that bridges FletX's routing configuration with Flet's
declarative ``ft.Router`` (available since Flet 0.85.0), while
preserving the FletX navigation DX (``navigate()``, ``go_back()``, etc.).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import flet as ft

from fletx.core.routing.config import RouterConfig
from fletx.core.routing.models import (
    NavigationResult,
    RouteInfo,
    NavigationMode,
)


_logger = logging.getLogger("FletX.FletBackend")


class FletRouterBackend:
    """
    Wraps Flet's ``ft.Router`` so it can be used as the routing engine
    underneath the familiar FletX navigation API.

    Requires **flet >= 0.85.0**.
    """

    def __init__(
        self,
        page: ft.Page,
        config: RouterConfig,
        initial_route: str = "/",
    ):
        self.page = page
        self._config = config
        self._initial_route = initial_route

        # -- state mirroring FletXRouter -----------------------------------
        self._current_route: RouteInfo = RouteInfo(path=initial_route)
        self._history: List[RouteInfo] = []
        self._forward_stack: List[RouteInfo] = []

        # -- built lazily in _ensure_router() ------------------------------
        self._router: Optional["ft.Router"] = None  # noqa: F821
        self._ready = False

    # -- public API (matches FletXRouter subset) ---------------------------

    def get_current_route(self) -> RouteInfo:
        return self._current_route

    async def navigate(
        self,
        route: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        replace: bool = False,
        clear_history: bool = False,
        **_kwargs,
    ) -> NavigationResult:
        self._ensure_router()
        if self._router is None:
            return NavigationResult.ERROR

        if clear_history:
            self._history.clear()
            self._forward_stack.clear()

        if not replace:
            self._history.append(self._current_route)
            self._forward_stack.clear()

        # ft.Router accepts a string route or a Route object
        await self._router.push(route)

        self._current_route = RouteInfo(
            path=route, data=data or {}
        )
        return NavigationResult.SUCCESS

    def go_back(self) -> bool:
        self._ensure_router()
        if not self._history or self._router is None:
            return False
        self._forward_stack.append(self._current_route)
        self._current_route = self._history.pop()
        self._router.pop()
        return True

    def go_forward(self) -> bool:
        self._ensure_router()
        if not self._forward_stack or self._router is None:
            return False
        self._history.append(self._current_route)
        self._current_route = self._forward_stack.pop()
        self._router.push(self._current_route.path)
        return True

    # -- internal setup -----------------------------------------------------

    def _ensure_router(self):
        """Lazy-init the ``ft.Router`` and attach it to the page."""
        if self._ready:
            return

        try:
            # ── late import so older Flet versions don't crash at import ──
            from flet import Router as FletRouter
            from flet import Route as FletRoute
        except ImportError:
            _logger.warning(
                "ft.Router is not available in this Flet version "
                "(requires >= 0.85.0). Falling back to FletXRouter."
            )
            self._ready = True  # mark as ready so callers don't retry
            return

        flet_routes: list = []
        for path, route_def in self._config.get_all_routes().items():
            component_cls = route_def.component

            # Wrap the FletXPage class in a @ft.component adapter
            @ft.component
            def _wrapper(page_class=component_cls):
                instance = page_class()
                return instance

            flet_routes.append(FletRoute(path=path, component=_wrapper))

        # Build the router component
        @ft.component
        def _app_with_router():
            return FletRouter(
                routes=flet_routes,
                initial_route=self._initial_route,
                manage_views=True,
            )

        # Mount it onto the page
        self.page.render_views(_app_with_router)
        self._ready = True
        _logger.info("Flet Router backend initialised.")
