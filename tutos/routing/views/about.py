import flet as ft
from fletx.core import FletXPage
from fletx.navigation import navigate
from views.footer import Footer


class AboutPage(FletXPage):
    def build(self):
        name = (self.route_info.data or {}).get("name", "") if self.route_info else ""
        greeting = ft.Text(
            f"Hello, {name} !" if name else "",
            size=22,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.BLUE_400,
        )
        return ft.Column(
            spacing=10,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=80),
                ft.Icon(ft.Icons.INFO_OUTLINE, size=64, color=ft.Colors.BLUE_400),
                ft.Container(height=20),
                ft.Text("About", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                greeting,
                ft.Container(height=8),
                ft.Text(
                    "FletX Routing Demo",
                    size=18,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=8),
                ft.Text(
                    "This tutorial demonstrates dynamic routing with FletX.\n"
                    "Navigate between pages using the FletX router.",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(expand=True),
                ft.Button(
                    "← Back to Home",
                    icon=ft.Icons.ARROW_BACK_IOS,
                    on_click=lambda e: navigate("/"),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=7)),
                ),
                ft.Container(height=20),
                Footer(),
            ],
        )
