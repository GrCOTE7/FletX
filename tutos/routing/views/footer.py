import sys

import flet as ft
from fletx import __version__ as fletx_version


class Footer(ft.Container):
    def __init__(self):
        python_version = (
            f"{sys.version_info.major}."
            f"{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        )

        super().__init__(
            height=100,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        f"🚀 Powered by FletX {fletx_version}",
                        color=ft.Colors.GREY_600,
                    ),
                    ft.Text(
                        f"Flet {ft.__version__} & Python {python_version}",
                        color=ft.Colors.GREY_600,
                    ),
                ],
            ),
        )


footer = Footer
