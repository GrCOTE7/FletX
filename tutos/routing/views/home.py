import flet as ft
from fletx.core import FletXPage
from fletx.navigation import navigate
from views.footer import Footer


class HomePage(FletXPage):
    def build(self):
        return ft.Column(
            spacing=10,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=100),
                ft.Image(src="logo.png", fit=ft.BoxFit.CONTAIN, width=120, height=120),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Welcome to the Home Page!",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Use the navigation to explore different pages.",
                                size=14,
                            ),
                            ft.Container(height=20),
                            ft.Button(
                                "Go to About",
                                icon=ft.Icons.INFO_OUTLINE,
                                on_click=lambda e: navigate("/about"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=7)
                                ),
                            ),
                        ],
                    ),
                ),
                Footer(),
            ],
        )
