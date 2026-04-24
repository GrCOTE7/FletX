import flet as ft
from typing import cast
from fletx.core import FletXPage
from fletx.widgets import Obx

from ..controllers.counter import CounterController
from ..components import MyReactiveText


class CounterPage(FletXPage):
    ctrl = CounterController()

    def build(self):
        return ft.Column(
            spacing=10,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=100),
                ft.Image(
                    src="logo.png", fit=ft.ImageFit.CONTAIN, width=120, height=120
                ),
                ft.Text("🚀 powered by FletX 0.1.4", color=ft.Colors.GREY_600),
                ft.Text("Python version 3.13", color=ft.Colors.GREY_600),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "DemoApp Counter", size=20, weight=ft.FontWeight.BOLD
                            ),
                            cast(
                                ft.Control,
                                Obx(
                                    builder_fn=lambda: ft.Text(
                                        value=f"{self.ctrl.count}",
                                        size=100,
                                        weight=ft.FontWeight.BOLD,
                                    )
                                ),
                            ),
                            ft.CupertinoFilledButton(
                                content=ft.Text("Increment"),
                                opacity_on_click=0.7,
                                padding=10,
                                on_click=lambda e: self.ctrl.count.increment(),  # Auto UI update
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    height=100,
                    content=ft.Text("Thanks for choosing FletX"),
                ),
            ],
        )
