"""
Obx - Reactive Builder Widget for FletX

Obx automatically tracks Reactive dependencies accessed during the
builder call and rebuilds the content whenever those dependencies change.
"""

from typing import Callable, Set, Optional, List

import flet as ft

from fletx.core.state import Reactive, ReactiveDependencyTracker, Observer
from fletx.utils import get_logger


class _ObxTracker:
    """Dependency tracker that feeds discovered reactives into Obx."""

    def __init__(self, obx: 'Obx'):
        self.obx = obx

    def add(self, reactive_obj: Reactive):
        self.obx._add_dependency(reactive_obj)


class _ObxContext:
    """Context manager that installs a custom dependency tracker."""

    def __init__(self, obx: 'Obx'):
        self.obx = obx
        self._previous_tracker = None

    def __enter__(self):
        self._previous_tracker = ReactiveDependencyTracker._current_tracker
        ReactiveDependencyTracker._current_tracker = _ObxTracker(self.obx)

    def __exit__(self, *args):
        ReactiveDependencyTracker._current_tracker = self._previous_tracker


class Obx(ft.Container):
    """
    Reactive wrapper that calls *builder_fn* to produce its content,
    automatically subscribes to every Reactive accessed during the call,
    and rebuilds when any of those dependencies change.

    Usage::

        class MyPage(FletXPage):
            def build(self):
                return ft.Column([
                    Obx(lambda: ft.Text(f"Count: {self.ctrl.count.value}")),
                ])
    """

    def __init__(
        self,
        builder_fn: Callable[[], ft.Control],
        **kwargs,
    ):
        self._builder_fn = builder_fn
        self._dependencies: Set[Reactive] = set()
        self._observers: List[Observer] = []
        self._is_mounted = False
        self._logger = get_logger("Obx")

        super().__init__(**kwargs)

        try:
            self.content = self._build_and_track()
        except Exception as e:
            self._logger.error(f"Obx builder failed during init: {e}")
            self.content = ft.Text("Obx error")

    # --- dependency management ------------------------------------------------

    def _add_dependency(self, reactive_obj: Reactive):
        if reactive_obj not in self._dependencies:
            observer = reactive_obj.listen(self._rebuild)
            self._dependencies.add(reactive_obj)
            if observer is not None:
                self._observers.append(observer)

    # --- build / rebuild ------------------------------------------------------

    def _build_and_track(self) -> ft.Control:
        """Run the builder inside a tracking context and return the result."""
        with _ObxContext(self):
            return self._builder_fn()

    def _rebuild(self):
        """Called when a tracked Reactive changes."""
        if not self._is_mounted:
            return
        try:
            self.content = self._build_and_track()
            self.update()
        except Exception as e:
            self._logger.error(f"Obx rebuild failed: {e}")

    # --- lifecycle ------------------------------------------------------------

    def did_mount(self):
        self._is_mounted = True
        super().did_mount()

    def will_unmount(self):
        self._is_mounted = False
        self.dispose()
        super().will_unmount()

    def dispose(self):
        for observer in self._observers:
            try:
                observer.dispose()
            except Exception:
                pass
        self._observers.clear()
        self._dependencies.clear()
