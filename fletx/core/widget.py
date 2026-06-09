"""
Base Widget for FletX

Base class for reactive FletX widgets. Provides lifecycle hooks
(build, did_mount, will_unmount) without any import-time side effects.
"""

from abc import ABC, abstractmethod
from typing import Union, List

import flet as ft
from fletx.utils import get_logger


class FletXWidget(ABC):
    """
    Base reactive widget mixin.
    Subclass this together with a flet Control to add FletX lifecycle.
    """

    _logger = get_logger('FletX.Widget')

    def __init__(self):
        self._is_mounted = False

    @abstractmethod
    def build(self) -> Union[ft.Control, List[ft.Control]]:
        """Build and return the widget content."""
        ...

    def did_mount(self):
        self._is_mounted = True

    def will_unmount(self):
        self._is_mounted = False

    def render(self) -> Union[ft.Control, List[ft.Control]]:
        try:
            return self.build()
        except Exception as e:
            self._logger.error(
                f"Error rendering {self.__class__.__name__}: {e}"
            )
            return ft.Text(f"Error: {e}", color=ft.Colors.RED)
