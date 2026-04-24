import flet as ft

def main(page: ft.Page):
    page.title = "Routing demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            margin=ft.Margin.only(top=25),
            controls=[
                ft.Text(
                    "ROUTING.",
                    size=30,
                    color=ft.Colors.CYAN_400,
                    weight=ft.FontWeight.BOLD,
                )
            ],
        )
    )
    
if __name__ == "__main__":
    # print(datetime.datetime.now().strftime("%H:%M:%S"), "> ")
    ft.app(target=main)
