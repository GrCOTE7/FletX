from re import A

import flet as ft
import datetime, time
import asyncio
import importlib.util
from pathlib import Path
from tools.screen_utils import gc7_rules as gc7


async def main(page: ft.Page, width: int = 392):
    # gc7(page, mode="LIGHT", name="Cookbook", width=900, height=700)
    # gc7(page, mode="LIGHT", width=width)

    # from examples.lv00_matrice import main as go
    # go(page)

    # from basis.scroll_example import main as scroll
    # scroll(page)

    # from basis.lv01_essai import essai as essai
    # essai(page)

    # # from examples.lv04_calc_ui import calc as calc
    # from examples.lv05_calc_ui_reusable import calc as calc
    # calc(page)

    # from devs.lv01_icons_list import icons_list as icons_list
    # icons_list(page) # 3 versions dispos

    # from devs.lv02_blocs import blocs as dev
    # dev(page)

    # # ❌ Finir game NbreX
    # from devs.lv05_nbre_x import game as game
    # game(page)

    # from cookbook.main import main as cookbook_main
    # gc7(page, width=976)
    # # gc7(page, "LIGHT", width=976)
    gc7(page)
    # cookbook_main(page)
    #
    #
    # from devs.lv10_tutos import ab_btn as demo_main  # label alternatif et btn adapté
    # try:
    #     from devs.lv10_tutos import tofs as demo_main  # label alternatif et btn adapté

    #     demo_main(page)
    # except ModuleNotFoundError as exc:
    #     if exc.name != "devs":
    #         raise

    ################################### ToDo ###################################

    # from examples.lv06_todo_simple import todo_list as todo6
    # todo6(page)

    # Test fonctions asynchones
    # if 0:
    #     from examples.lv07_todo_async import todo_list as todo7
    #     from examples.lv06_async_todo_simple import todo_list as todo6_async

    #     async def fini():
    #         print(
    #             datetime.datetime.now().strftime("%H:%M:%S"), "> Todos 6 & 7 Ready.\n"
    #         )

    #     async def async_fctns():
    #         print(datetime.datetime.now().strftime("%H:%M:%S"), "> async_fctns")
    #         await asyncio.gather(todo6_async(page), todo7(page))
    #         await fini()

    #     await async_fctns()
    #     time.sleep(1)

    # from examples.lv08_todo import todo_list as todo8
    # todo8(page)

    # from examples.lv09_todo_simple import todo9 as todo9
    # todo9(page)

    # from examples.lv09_todo import todo_list as todo9
    # todo9(page)

    # page.add(ft.Text('─'*49))

    # from examples.lv10_todo import todo as finalTodo
    # gc7(page, width=950)
    # finalTodo(page)

    # from examples.lv11_todo import main as finalTodo  # + Footer
    # finalTodo(page)

    # from examples.lv11_todo_official import main as finalTodo
    # gc7(page, "LIGHT", width=600)
    # finalTodo(page)

    # * [ ] LV 12 à comprendre pour incorporer ici
    # ⚠️ render_views prend le contrôle total de la page → ne pas mélanger avec page.add()
    # from examples.lv12_todo_reactive import main as reactivTodo
    # reactivTodo(page)
    # return  # render_views incompatible avec page.controls / page.add() ci-dessous

    ################################### CHAT ###################################

    # * [/] chat

    # from examples.lv20_chat import main  # Base
    # from examples.lv21_chat import main  # Add pubsub.subscribe ( Broadcasting)
    # from examples.lv22_chat import main  # Login ( + auto login )
    # from examples.lv23_chat import main  # Class + ↑ User msg look
    # from examples.lv24_chat import main  # SIMU login & msgs Scrolling auto

    # gc7(page, "LIGHT")
    # main(page)

    ################################ SOLITAIRE  ################################

    # from examples.lv30_a1_stack import main  # 3 image blocs
    # from examples.lv30_a2_stack import main  # 3 cards (Bleu-blanc-rouge)
    # from examples.lv30_a3_stack import main  # A card on a tapis

    # gc7(page, mode="LIGHT", width=976)  # 976 pour // 2 l'écran de droite

    # from examples.lv30_solitaire import main  # GestureDetector (on_tap)
    # from examples.lv31_solitaire import main  # drag a card
    # from examples.lv32_solitaire import main  # drag to slot
    # from examples.lv33_solitaire import main  # drag a card on a slot else return back position

    # drag 2 cards with pans
    # from examples.lv34_solitaire import main

    # drop in 3 slots
    # from examples.lv35_solitaire import main

    # Classes for better code structure (POO)
    # from examples.lv36_main import main

    # Fanned cards piles (Piles en éventail)
    # from examples.lv37_main import main

    # Solitaire setup
    # from examples.lv38_main import main

    # * [/] Solitaire general rules
    # from examples.lv39_main import main
    #
    # from cookbook.main import main as cookbook_main
    # # gc7(page, width=976)
    # # gc7(page, "LIGHT", width=976)
    # cookbook_main(page)
    #

    # ❌  Le seul qui corrige le pb de double clic → Le comprendre complètement à la fin - D:\flet_doc\sdk\python\examples\tutorials\solitaire_declarative\solitaire-final\main.py

    # from devs.lv00_dev import dev as dev
    # dev(page)

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
