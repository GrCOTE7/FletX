from fletx.cli.commands.base import FletPassthroughCommand


class BuildCommand(FletPassthroughCommand):
    """Build a Flet app with PyInstaller."""

    command_name = "build"
    flet_subcommand = "build"


class DebugCommand(FletPassthroughCommand):
    """Debug a Flet app on a connected device or emulator."""

    command_name = "debug"
    flet_subcommand = "debug"


class PackCommand(FletPassthroughCommand):
    """Package a Flet app into an executable."""

    command_name = "pack"
    flet_subcommand = "pack"


class PublishCommand(FletPassthroughCommand):
    """Publish a Flet web app."""

    command_name = "publish"
    flet_subcommand = "publish"


class ServeCommand(FletPassthroughCommand):
    """Serve static files for a Flet web app."""

    command_name = "serve"
    flet_subcommand = "serve"


class EmulatorsCommand(FletPassthroughCommand):
    """List, create, and launch emulators."""

    command_name = "emulators"
    flet_subcommand = "emulators"


class DevicesCommand(FletPassthroughCommand):
    """List connected mobile devices."""

    command_name = "devices"
    flet_subcommand = "devices"


class DoctorCommand(FletPassthroughCommand):
    """Show system and environment info for debugging."""

    command_name = "doctor"
    flet_subcommand = "doctor"
