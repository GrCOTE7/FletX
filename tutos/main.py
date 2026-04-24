from re import A

import flet as ft
import datetime, time
import asyncio
import importlib.util
from pathlib import Path
from tools.screen_utils import gc7_rules as gc7


async def main(page: ft.Page, width: int = 392):
    # gc7(page, mode="LIGHT", name="Cookbook", width=900, height=700)
    # gc7(page, width=976)
    # gc7(page, mode="LIGHT", width=width)
    
    left = "Activer pour App sur la droite d'1 écran unique"
    
    gc7(page, left=1520 if "left" in locals() else 1912, width=width)

    ################################## Routing #################################
    # from routing.template import main
    # main(page)
    from routing.main import RoutingDemoRouter  # noqa: F401 — registers the router
    from fletx.app import FletXApp

    _app = FletXApp(title="FletX Routing Demo", initial_route="/", debug=True)
    await _app._async_main(page)
    return
    ################################### Other ##################################

    if not page.controls:
        page.add(
            ft.Container(
                margin=ft.Margin.only(top=30),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "No content.",
                            size=30,
                            color=ft.Colors.RED_ACCENT_200,
                            weight=ft.FontWeight.BOLD,
                        )
                    ],
                ),
            )
        )


if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%H:%M:%S"), "> ")
    ft.run(main)
