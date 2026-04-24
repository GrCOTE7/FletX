"""
DemoApp App
None

A FletX application.
Author: Developer
Version: 0.1.0
"""

import flet as ft
from fletx.app import FletXApp
from app.routes import DemoAppRouter
from app.utils.theme import light_theme, dark_theme


def main():
    """Main entry point for the DemoApp application."""

    # Lifecycle Hooks
    async def on_startup(page: ft.Page):
        print("App is running!")

    def on_shutdown(page: ft.Page):
        print("App is closed!")

    # App Configuration
    app = FletXApp(
        title="DemoApp",
        initial_route="/",
        debug=True,
        theme=light_theme,
        dark_theme=dark_theme,
        theme_mode=ft.ThemeMode.SYSTEM,
        window_config={
            "width": 396,
            "height": 810,
            "resizable": True,
            "maximizable": True,
        },
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )

    # Run App
    app.run_async()  # you can use also `app.run()` method. see documetation for more


if __name__ == "__main__":
    main()
