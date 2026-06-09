"""
Tests for the rewritten Obx reactive widget.
"""

from typing import List

import flet as ft
import pytest

from fletx.core.state import Reactive, RxInt, RxStr
from fletx.widgets.obx import Obx


class TestObxDependencyTracking:
    """Obx must detect Reactive dependencies accessed during builder calls."""

    def test_initial_content_from_builder(self):
        """Builder result appears as Obx.content immediately."""
        rx = RxInt(42)
        obx = Obx(lambda: ft.Text(f"Value: {rx.value}"))
        assert obx.content is not None
        assert str(obx.content.value) == "Value: 42"

    def test_dependencies_populated(self):
        """Every Reactive accessed in the builder is tracked."""
        rx = RxInt(0)
        obx = Obx(lambda: ft.Text(str(rx.value)))
        assert rx in obx._dependencies

    def test_multiple_dependencies(self):
        """Multiple Reactives are all tracked."""
        a = RxInt(1)
        b = RxStr("hello")
        obx = Obx(lambda: ft.Column([
            ft.Text(str(a.value)),
            ft.Text(b.value),
        ]))
        assert a in obx._dependencies
        assert b in obx._dependencies

    def test_tracking_across_rebuild(self):
        """Re-running the builder does not lose existing dependencies."""
        rx = RxInt(0)
        obx = Obx(lambda: ft.Text(str(rx.value)))
        _ = obx._build_and_track()
        assert rx in obx._dependencies

    def test_rebuild_triggered_when_mounted(self, monkeypatch):
        """_rebuild is called when a tracked Reactive changes and is mounted."""
        rx = RxInt(0)

        rebuild_called = False

        def patched_rebuild(self):
            nonlocal rebuild_called
            rebuild_called = True

        # Patch on the class so the bound method reference uses the patched one
        monkeypatch.setattr(Obx, "_rebuild", patched_rebuild)

        obx = Obx(lambda: ft.Text(str(rx.value)))
        obx._is_mounted = True

        rebuild_called = False
        rx.value = 1
        assert rebuild_called, "_rebuild was not called after reactive changed"

    def test_dispose_cleans_up(self):
        """dispose() removes all listeners and clears dependencies."""
        rx = RxInt(0)
        obx = Obx(lambda: ft.Text(str(rx.value)))

        assert len(obx._dependencies) == 1
        assert len(obx._observers) == 1

        obx.dispose()

        assert len(obx._dependencies) == 0
        assert len(obx._observers) == 0

    def test_dispose_prevents_further_rebuilds(self):
        """After dispose, changes to dependencies do not trigger rebuild."""
        rx = RxInt(0)
        obx = Obx(lambda: ft.Text(str(rx.value)))

        original_content = obx.content
        obx.dispose()

        rx.value = 99
        assert obx.content is original_content

    def test_builder_error_handling(self):
        """If the builder raises, Obx falls back to an error text."""
        def broken_builder():
            raise ValueError("oops")

        obx = Obx(broken_builder)
        assert obx.content is not None
        assert "error" in str(obx.content.value).lower()

    def test_rebuild_skipped_when_not_mounted(self):
        """_rebuild does nothing when _is_mounted is False."""
        rx = RxInt(0)
        obx = Obx(lambda: ft.Text(str(rx.value)))
        # _is_mounted is False by default
        original = obx.content
        rx.value = 42
        assert obx.content is original

    def test_rebuild_skipped_does_not_add_duplicate_deps(self):
        """Repeated rebuilds do not duplicate dependencies."""
        rx = RxInt(0)
        obx = Obx(lambda: ft.Text(str(rx.value)))
        initial_count = len(obx._dependencies)
        for _ in range(5):
            _ = obx._build_and_track()
        assert len(obx._dependencies) == initial_count


class TestObxContentUpdate:
    """Verify that content actually changes after a rebuild."""

    def test_content_text_updates_via_rebuild(self, monkeypatch):
        """When Reactive value changes, Obx content reflects the new value."""
        rx = RxInt(0)

        call_count = 0
        captured_values: List[str] = []

        def builder():
            nonlocal call_count
            call_count += 1
            val = str(rx.value)
            captured_values.append(val)
            return ft.Text(val)

        # Patch _rebuild at class level so listeners use it
        def patched_rebuild(self):
            if not self._is_mounted:
                return
            try:
                self.content = self._build_and_track()
            except Exception as e:
                pass

        monkeypatch.setattr(Obx, "_rebuild", patched_rebuild)

        obx = Obx(builder)
        assert call_count == 1
        assert captured_values == ["0"]

        obx._is_mounted = True

        rx.value = 42

        assert call_count == 2
        assert captured_values == ["0", "42"]
        assert str(obx.content.value) == "42"
