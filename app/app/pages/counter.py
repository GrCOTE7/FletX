import flet as ft
from fletx.core import FletXPage

from ..controllers.counter import CounterController


class CounterPage(FletXPage):
    ctrl = CounterController()

    def _increment_counter(self, e: ft.ControlEvent):
        self.ctrl.count.increment()
        self._build_page()
        self.refresh()

    def build(self):
        return ft.Column(
            spacing=10,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=100),
                ft.Image(src="logo.png", fit=ft.BoxFit.CONTAIN, width=120, height=120),
                ft.Text("🚀 powered by FletX 0.1.4", color=ft.Colors.GREY_600),
                ft.Text("Python version 3.13", color=ft.Colors.GREY_600),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "DemoApp Counter", size=20, weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                value=str(self.ctrl.count.value),
                                size=100,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.CupertinoFilledButton(
                                content=ft.Text("Increment"),
                                opacity_on_click=0.7,
                                padding=10,
                                on_click=self._increment_counter,
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
