"""
FletX Navigation API.

Convenience functions that work transparently with both the built-in
``FletXRouter`` and the optional ``ft.Router`` backend.
"""

import asyncio
from typing import Any, Dict, Optional

from fletx.core.routing.router import FletXRouter
from fletx.core.routing.config import (
    RoutePattern, RouterConfig, router_config,
    ModuleRouter,
)
from fletx.core.routing.guards import RouteGuard
from fletx.core.routing.middleware import RouteMiddleware
from fletx.core.routing.transitions import TransitionType, RouteTransition
from fletx.core.routing.models import (
    RouteInfo, RouterState, RouteType,
    NavigationIntent, NavigationMode,
    NavigationResult, IRouteResolver,
)
from fletx.utils import get_event_loop, run_async, get_logger
from fletx.utils.context import AppContext


def _resolve_backend():
    """Return the active routing backend (FletXRouter or FletRouterBackend)."""
    flet_backend = AppContext.get_data("router_backend")
    if flet_backend is not None:
        return flet_backend
    return FletXRouter.get_instance()


def get_router():
    """Get the current routing backend instance."""
    return _resolve_backend()


async def navigate_to(route: str, **kwargs) -> NavigationResult:
    """Navigate using the global router."""
    router = _resolve_backend()
    try:
        if hasattr(router, "navigate"):
            result = await router.navigate(route, **kwargs)
        else:
            result = await router.navigate(route, **kwargs)
        return result
    except asyncio.CancelledError:
        get_logger("FletX.Navigation").warning("Navigation was cancelled")
        return NavigationResult.CANCELLED


def navigate(route: str, **kwargs) -> Optional[NavigationResult]:
    """Synchronous wrapper for navigation."""
    return run_async(lambda: navigate_to(route, **kwargs))


def go_back() -> bool:
    """Go back using the global router."""
    return _resolve_backend().go_back()


def go_forward() -> bool:
    """Go forward using the global router."""
    return _resolve_backend().go_forward()


def get_current_route() -> RouteInfo:
    """Get current route information."""
    return _resolve_backend().get_current_route()


__all__ = [
    "RouteGuard",
    "RouteMiddleware",
    "TransitionType",
    "RouteTransition",
    "RoutePattern",
    "RouterConfig",
    "FletXRouter",
    "NavigationResult",
    "RouteInfo",
    "RouterState",
    "RouteType",
    "NavigationIntent",
    "NavigationMode",
    "IRouteResolver",
    "ModuleRouter",
    "router_config",
    "get_router",
    "navigate",
    "navigate_to",
    "go_back",
    "go_forward",
    "get_current_route",
]
