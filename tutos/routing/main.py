import sys
from pathlib import Path

# Ensure this file's directory is on sys.path so 'views' is always found.
sys.path.insert(0, str(Path(__file__).parent))

from fletx.app import FletXApp
from fletx.navigation import ModuleRouter
from fletx.decorators import register_router

from views.home import HomePage
from views.about import AboutPage


@register_router
class RoutingDemoRouter(ModuleRouter):
    name = "routing_demo"
    base_path = "/"
    is_root = True
    routes = [
        {"path": "/", "component": HomePage},
        {"path": "/about", "component": AboutPage},
    ]
    sub_routers = []


def run_app():
    app = FletXApp(
        title="FletX Routing Demo",
        initial_route="/",
        debug=True,
    )
    app.run_async()


if __name__ == "__main__":
    run_app()
