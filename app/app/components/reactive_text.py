import flet as ft
from fletx.core import (
    RxStr
)
from fletx.decorators import (
    simple_reactive
)

@simple_reactive(
    bindings={
        'value': 'text'
    }
)
class MyReactiveText(ft.Text):
    """My Reactive Text Widget"""
    def __init__(self, rx_text: RxStr, **kwargs):
        self.text: RxStr = rx_text
        print(self.text.value)
        super().__init__(**kwargs)
